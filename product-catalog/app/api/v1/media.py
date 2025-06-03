from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.media import Media
from app.models.schemas.media import MediaCreate, MediaInDB
from app.core.auth import require_roles
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/products/{product_id}/media", response_model=MediaInDB, tags=["media"])
def add_media(product_id: int, media: MediaCreate, db: Session = Depends(get_db), user=Depends(require_roles(["admin", "seller"]))):
    db_media = Media(product_id=product_id, **media.dict())
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return db_media

@router.get("/products/{product_id}/media", response_model=List[MediaInDB], tags=["media"])
def get_media(product_id: int, db: Session = Depends(get_db)):
    return db.query(Media).filter(Media.product_id == product_id).order_by(Media.position).all()

@router.delete("/media/{media_id}", tags=["media"])
def delete_media(media_id: int, db: Session = Depends(get_db), user=Depends(require_roles(["admin", "seller"]))):
    db_media = db.query(Media).filter(Media.media_id == media_id).first()
    if not db_media:
        raise HTTPException(status_code=404, detail="Media not found")
    db.delete(db_media)
    db.commit()
    return {"ok": True}
