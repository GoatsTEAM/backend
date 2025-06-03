import asyncio
from app.db.database import SessionLocal
from app.models.product import Product
from app.models.media import Media
from app.services.search_client import index_product

import logging
import time
import json
import requests

def send_user_activity(event_type, user_id, product_id=None, extra=None):
    logging.info(f"User activity: {event_type}, user_id={user_id}, product_id={product_id}, extra={extra}")
    pass

def stream_product_media(storage_key):
    logging.info(f"Streaming media from storage: {storage_key}")
    pass

def log_metric(metric_name, value, labels=None):
    logging.info(f"Metric: {metric_name}={value}, labels={labels}")
    pass

def trace_event(event_name, attributes=None):
    logging.info(f"Trace: {event_name}, attributes={attributes}")
    pass

async def etl_sync():
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        for product in products:
            media = db.query(Media).filter(Media.product_id == product.id).all()
            product_dict = {
                "id": product.id,
                "title": product.title,
                "description": product.description,
                "price": product.price,
                "stock_quantity": product.stock_quantity,
                "category_id": product.category_id,
                "seller_id": product.seller_id,
                "created_at": str(product.created_at),
                "updated_at": str(product.updated_at),
                "media": [
                    {
                        "media_id": m.media_id,
                        "storage_key": m.storage_key,
                        "media_type": m.media_type,
                        "position": m.position,
                        "metadata": m.metadata,
                    } for m in media
                ]
            }
            await index_product(product_dict)
    finally:
        db.close()

async def sync_to_search_engine(product_id: int):
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return
        media = db.query(Media).filter(Media.product_id == product.id).all()
        product_dict = {
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "price": product.price,
            "stock_quantity": product.stock_quantity,
            "category_id": product.category_id,
            "seller_id": product.seller_id,
            "created_at": str(product.created_at),
            "updated_at": str(product.updated_at),
            "media": [
                {
                    "media_id": m.media_id,
                    "storage_key": m.storage_key,
                    "media_type": m.media_type,
                    "position": m.position,
                    "metadata": m.metadata,
                } for m in media
            ]
        }
        await index_product(product_dict)
    finally:
        db.close()
