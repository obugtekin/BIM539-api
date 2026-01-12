from fastapi import APIRouter, HTTPException
from database import get_db
from models import Category, CategoryCreate, CategoryUpdate
import sqlite3

router = APIRouter()

@router.get("/", summary="Tüm kategorileri listele")
def get_categories():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categories")
    rows = cursor.fetchall()
    db.close()
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "created_at": row[3]
        })
    return result

@router.get("/{category_id}", summary="ID'ye göre kategori getir")
def get_category(category_id: int):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
    row = cursor.fetchone()
    db.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Kategori bulunamadı")
    
    return {"id": row[0], "name": row[1], "description": row[2], "created_at": row[3]}

@router.post("/", status_code=201, summary="Yeni kategori oluştur")
def create_category(category: CategoryCreate):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO categories (name, description, created_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
            (category.name, category.description)
        )
        db.commit()
        
        last_id = cursor.lastrowid
        cursor.execute("SELECT * FROM categories WHERE id = ?", (last_id,))
        row = cursor.fetchone()
        db.close()
        return {"id": row[0], "name": row[1], "description": row[2], "created_at": row[3]}
    except Exception as e:
        db.close()
        raise HTTPException(status_code=400, detail="Kategori oluşturma hatası")

@router.patch("/{category_id}", summary="Kategori bilgilerini güncelle")
def update_category(category_id: int, category_update: CategoryUpdate):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
    current = cursor.fetchone()
    if not current:
        db.close()
        raise HTTPException(status_code=404, detail="Kategori bulunamadı")
    
    if category_update.name is not None:
        name = category_update.name
    else:
        name = current[1]
    
    if category_update.description is not None:
        description = category_update.description
    else:
        description = current[2]
    
    try:
        cursor.execute(
            "UPDATE categories SET name=?, description=? WHERE id=?",
            (name, description, category_id)
        )
        db.commit()
        
        cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        row = cursor.fetchone()
        db.close()
        return {"id": row[0], "name": row[1], "description": row[2], "created_at": row[3]}
    except Exception as e:
        db.close()
        raise HTTPException(status_code=400, detail="Güncelleme hatası")

@router.delete("/{category_id}", summary="Kategoriyi sil")
def delete_category(category_id: int):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
    if not cursor.fetchone():
        db.close()
        raise HTTPException(status_code=404, detail="Kategori bulunamadı")
    
    cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
    db.commit()
    db.close()
    
    return {"message": "Kategori başarıyla silindi"}
