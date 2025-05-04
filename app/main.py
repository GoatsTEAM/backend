# app/main.py
import asyncio
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Float,
    ForeignKey,
    JSON,
    DateTime,
    delete,
    select,
    func
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID as PGUUID
import redis

# ---------- Заглушки для временных реализаций ----------
class KafkaProducerStub:
    def produce(self, topic, key=None, value=None):
        print(f"Kafka stub: Sent to {topic}, key: {key}, value: {value[:50]}...")

class ElasticsearchClientStub:
    async def index(self, index, id, body):
        print(f"Elasticsearch stub: Indexed {id} in {index}")

# ---------- Database Setup ----------
DATABASE_URL = "postgresql+asyncpg://catalog_user:strong_password@localhost/product_catalog"
engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# ---------- Redis Setup ----------
redis_client = redis.Redis()  # Подключение к локальному Redis

# ---------- Kafka Setup ----------
kafka_producer = KafkaProducerStub()

# ---------- Models ----------
class Product(Base):
    __tablename__ = "products"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    description = Column(String)
    base_price = Column(Float, nullable=False)
    seller_id = Column(PGUUID(as_uuid=True), nullable=False)
    status = Column(String(20), default='draft')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    categories = relationship("ProductCategory", back_populates="product")
    attributes = relationship("ProductAttribute", back_populates="product")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    parent_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey('categories.id', ondelete="SET NULL"),
        nullable=True
    )
    name = Column(String(100), nullable=False)
    description = Column(String)
    
    children = relationship("Category", back_populates="parent")
    products = relationship("ProductCategory", back_populates="category")  # Новая строка
    parent = relationship("Category", remote_side=[id])  # Обновите relationship

class ProductCategory(Base):
    __tablename__ = "product_categories"
    
    product_id  = Column(PGUUID(as_uuid=True), ForeignKey('products.id',  ondelete="CASCADE"), primary_key=True)
    category_id = Column(PGUUID(as_uuid=True), ForeignKey('categories.id', ondelete="CASCADE"), primary_key=True)
    
    product = relationship("Product", back_populates="categories")
    category = relationship("Category", back_populates="products") 

class ProductAttribute(Base):
    __tablename__ = "product_attributes"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    product_id = Column(PGUUID(as_uuid=True), ForeignKey('products.id'))
    attribute_key = Column(String(100), nullable=False)
    attribute_value = Column(JSON, nullable=False)
    
    product = relationship("Product", back_populates="attributes")

# ---------- Schemas ----------
class ProductCreate(BaseModel):
    name: str
    description: str
    base_price: float
    categories: List[UUID]
    attributes: dict

class ProductResponse(ProductCreate):
    id: UUID
    seller_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime

class CategoryCreate(BaseModel):
    name: str
    parent_id: Optional[UUID] = None
    description: Optional[str] = None

# ---------- Services ----------
async def get_db():
    async with async_session() as session:
        yield session

# Заглушка для аутентификации
async def get_current_seller():
    return uuid4()  # Возвращаем фиктивный UUID продавца

class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def create_product(self, product_data: ProductCreate, seller_id: UUID):
        if product_data.base_price <= 0:
            raise HTTPException(status_code=400, detail="Invalid price")
            
        product = Product(
            **product_data.dict(exclude={'categories', 'attributes'}),
            seller_id=seller_id
        )
        
        for category_id in product_data.categories:
            product.categories.append(ProductCategory(category_id=category_id))
            
        for key, value in product_data.attributes.items():
            product.attributes.append(ProductAttribute(
                attribute_key=key,
                attribute_value=value
            ))
            
        self.db.add(product)
        await self.db.commit()
        self._send_to_search_index(product)
        self._update_cache(product)
        return product
        
    def _send_to_search_index(self, product: Product):
        kafka_producer.produce(
            'products',
            key=str(product.id),
            value=product.json()
        )
        
    def _update_cache(self, product: Product):
        redis_client.setex(
            f"product:{product.id}",
            3600,
            product.json()
        )

    async def update_product(self, product_id: UUID, update_data: dict, seller_id: UUID):
        product = await self.db.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        if product.seller_id != seller_id:
            raise HTTPException(status_code=403, detail="Forbidden")
        
        for key, value in update_data.items():
            if key in ['categories', 'attributes']:
                continue  # Обрабатываем отдельно
            setattr(product, key, value)
        
        # Обновление категорий
        if 'categories' in update_data:
            await self.db.execute(
                delete(ProductCategory).where(ProductCategory.product_id == product_id)
            )
            product.categories = [
                ProductCategory(category_id=cat_id) 
                for cat_id in update_data['categories']
            ]
        
        # Обновление атрибутов
        if 'attributes' in update_data:
            await self.db.execute(
                delete(ProductAttribute).where(ProductAttribute.product_id == product_id)
            )
            product.attributes = [
                ProductAttribute(attribute_key=k, attribute_value=v)
                for k, v in update_data['attributes'].items()
            ]
        
        product.updated_at = datetime.utcnow()
        await self.db.commit()
        
        # Асинхронные операции
        self._send_to_search_index(product)
        self._update_cache(product)
        return product
    
    async def delete_product(self, product_id: UUID, seller_id: UUID):
        product = await self.db.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404)
        
        if product.seller_id != seller_id:
            raise HTTPException(status_code=403)
        
        await self.db.delete(product)
        await self.db.commit()
        
        # Асинхронное удаление из кэша и поиска
        redis_client.delete(f"product:{product_id}")
        kafka_producer.produce('product_deleted', key=str(product_id))
    
    async def list_products(
        self,
        seller_id: Optional[UUID] = None,
        category_id: Optional[UUID] = None,
        page: int = 1,
        limit: int = 100
    ):
        query = select(Product)
        
        if seller_id:
            query = query.where(Product.seller_id == seller_id)
            
        if category_id:
            query = query.join(ProductCategory).where(
                ProductCategory.category_id == category_id
            )
            
        result = await self.db.execute(
            query.offset((page-1)*limit).limit(limit)
        )
        return result.scalars().all()
    
class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def update_category(self, category_id: UUID, update_data: dict):
        category = await self.db.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404)
        
        for key, value in update_data.items():
            setattr(category, key, value)
        
        await self.db.commit()
        return category
    
    async def delete_category(self, category_id: UUID):
        category = await self.db.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404)
        
        # Проверка на наличие дочерних категорий
        if category.children:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete category with subcategories"
            )
            
        # Проверка на использование в товарах
        product_count = await self.db.execute(
            select(func.count()).select_from(ProductCategory).where(
                ProductCategory.category_id == category_id
            )
        )
        if product_count.scalar() > 0:
            raise HTTPException(
                status_code=400,
                detail="Category is used in products"
            )
        
        await self.db.delete(category)
        await self.db.commit()
        return {"status": "deleted"}
    
    async def get_category_tree(self, parent_id: Optional[UUID] = None):
        query = select(Category).where(Category.parent_id == parent_id)
        result = await self.db.execute(query)
        categories = result.scalars().all()
        
        return [
            {
                **cat.__dict__,
                "children": await self.get_category_tree(cat.id)
            }
            for cat in categories
        ]

# ---------- API Endpoints ----------
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    # 1) Создаём таблицы в схеме public
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all,
            tables=[
                Product.__table__,
                Category.__table__,
                ProductCategory.__table__,
                ProductAttribute.__table__
            ]
        )

    # 2) Запускаем фоновую задачу по обновлению поискового индекса
    asyncio.create_task(update_search_index())

@app.post("/products", response_model=ProductResponse)
async def create_product(
    product_data: ProductCreate,
    seller_id: UUID = Depends(get_current_seller)
):
    async with async_session() as session:
        service = ProductService(session)
        return await service.create_product(product_data, seller_id)

@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: UUID):
    # Check cache first
    cached = redis_client.get(f"product:{product_id}")
    if cached:
        return cached
    
    async with async_session() as session:
        product = await session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404)
        return product

@app.post("/categories")
async def create_category(category_data: CategoryCreate):
    async with async_session() as session:
        category = Category(**category_data.dict())
        session.add(category)
        await session.commit()
        return category
    

@app.put("/products/{product_id}")
async def update_product(
    product_id: UUID,
    update_data: ProductCreate,
    seller_id: UUID = Depends(get_current_seller)
):
    async with async_session() as session:
        service = ProductService(session)
        return await service.update_product(product_id, update_data.dict(), seller_id)

@app.delete("/products/{product_id}")
async def delete_product(
    product_id: UUID,
    seller_id: UUID = Depends(get_current_seller)
):
    async with async_session() as session:
        service = ProductService(session)
        return await service.delete_product(product_id, seller_id)

@app.get("/products")
async def list_products(
    seller_id: Optional[UUID] = None,
    category_id: Optional[UUID] = None,
    page: int = 1,
    limit: int = 100
):
    async with async_session() as session:
        service = ProductService(session)
        return await service.list_products(seller_id, category_id, page, limit)

@app.put("/categories/{category_id}")
async def update_category(
    category_id: UUID,
    category_data: CategoryCreate
):
    async with async_session() as session:
        service = CategoryService(session)
        return await service.update_category(category_id, category_data.dict())

@app.delete("/categories/{category_id}")
async def delete_category(category_id: UUID):
    async with async_session() as session:
        service = CategoryService(session)
        return await service.delete_category(category_id)

@app.get("/categories/tree")
async def get_category_tree(parent_id: Optional[UUID] = None):
    async with async_session() as session:
        service = CategoryService(session)
        return await service.get_category_tree(parent_id)

# ---------- Background Tasks ----------
elasticsearch_client = ElasticsearchClientStub()

async def update_search_index():
    while True:
        await asyncio.sleep(5)
        print("Background task: Updating search index...")