
import psycopg2
import json
from elasticsearch import Elasticsearch, helpers

# Конфигурация PostgreSQL
PG_HOST = "localhost"
PG_PORT = 5432
PG_DB   = "your_database"
PG_USER = "your_user"
PG_PASS = "your_password"

ES_HOST = "http://localhost:9200"
INDEX_NAME = "products_index"

def get_postgres_connection():
    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASS
    )
    return conn

def fetch_products_with_related(conn):
    """
    Извлекаем из PostgreSQL все необходимые поля для products + seller + category (с именем родителя)
    """
    sql = """
    SELECT
      p.product_id,
      p.title,
      p.description,
      p.price,
      p.stock_quantity,
      p.created_at,
      p.updated_at,

      s.seller_id AS seller_seller_id,
      s.company_name AS seller_company_name,
      s.rating     AS seller_rating,

      c.category_id        AS category_category_id,
      c.name               AS category_name,
      c.parent_category_id AS category_parent_id,

      pc.name AS parent_category_name
    FROM products p
    LEFT JOIN sellers s ON p.seller_id = s.seller_id
    LEFT JOIN categories c ON p.category_id = c.category_id
    LEFT JOIN categories pc ON c.parent_category_id = pc.category_id;
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        cols = [desc[0] for desc in cur.description]
        for row in cur.fetchall():
            yield dict(zip(cols, row))

def fetch_media_map(conn):
    """
    Возвращает словарь: product_id -> список JSON-объектов media
    """
    media_sql = """
    SELECT
      m.product_id,
      jsonb_agg(
        jsonb_build_object(
          'media_id', m.media_id,
          'storage_key', m.storage_key,
          'media_type', m.media_type,
          'position', m.position,
          'metadata', m.metadata
        ) ORDER BY m.position
      ) AS media_array
    FROM media m
    GROUP BY m.product_id;
    """
    media_map = {}
    with conn.cursor() as cur:
        cur.execute(media_sql)
        for product_id, media_array in cur.fetchall():
            media_map[product_id] = media_array  # media_array — уже JSONB в виде Python-объекта
    return media_map

def generate_actions_to_es(products_rows, media_map):
    """
    Генератор для helpers.bulk: превращает каждую строку в action-документ.
    """
    for row in products_rows:
        pid = row["product_id"]
        
        # Структурируем вложенные объекты:
        seller = {
            "seller_id": row.get("seller_seller_id"),
            "company_name": row.get("seller_company_name"),
            "rating": float(row.get("seller_rating")) if row.get("seller_rating") is not None else None
        }
        category = {
            "category_id": row.get("category_category_id"),
            "name": row.get("category_name"),
            "parent_category_id": row.get("category_parent_id"),
            "parent_category_name": row.get("parent_category_name")
        }
        media_list = media_map.get(pid, [])
        
        doc = {
            "product_id": pid,
            "title": row.get("title"),
            "description": row.get("description"),
            "price": float(row.get("price")) if row.get("price") is not None else None,
            "stock_quantity": row.get("stock_quantity"),
            "created_at": row.get("created_at").isoformat() if row.get("created_at") else None,
            "updated_at": row.get("updated_at").isoformat() if row.get("updated_at") else None,

            "seller": seller,
            "category": category,
            "media": media_list
        }

        yield {
            "_index": INDEX_NAME,
            "_id": pid,     # используем product_id как id в ES
            "_source": doc
        }

def main():
    conn = get_postgres_connection()

    try:
        products_iter = fetch_products_with_related(conn)
        media_map = fetch_media_map(conn)

        es = Elasticsearch(ES_HOST)

        if not es.indices.exists(index=INDEX_NAME):
            raise RuntimeError(f"Индекс {INDEX_NAME} не существует. Сначала запустите es_setup.py")

        # Используем bulk-загрузку
        helpers.bulk(es, generate_actions_to_es(products_iter, media_map))
        print("Indexing completed.")

    finally:
        conn.close()

if __name__ == "__main__":
    main()