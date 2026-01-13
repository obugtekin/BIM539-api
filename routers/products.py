from fastapi import APIRouter, HTTPException
from database import get_db
from models import Product, ProductCreate, ProductUpdate
import sqlite3

router = APIRouter()

@router.get("/", summary="Tüm ürünleri listele")
def get_products():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    db.close()
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "price": row[3],
            "stock": row[4],
            "category_id": row[5],
            "created_at": row[6],
            "updated_at": row[7]
        })
    return result

@router.get("/{product_id}", summary="ID'ye göre ürün getir")
def get_product(product_id: int):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    db.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    
    return {"id": row[0], "name": row[1], "description": row[2], "price": row[3], 
            "stock": row[4], "category_id": row[5], "created_at": row[6], "updated_at": row[7]}

@router.post("/", status_code=201, summary="Yeni ürün oluştur")
def create_product(product: ProductCreate):
    db = get_db()
    cursor = db.cursor()
    
    if product.category_id:
        cursor.execute("SELECT * FROM categories WHERE id = ?", (product.category_id,))
        if not cursor.fetchone():
            db.close()
            raise HTTPException(status_code=400, detail="Geçersiz kategori ID'si")
    
    try:
        cursor.execute(
            "INSERT INTO products (name, description, price, stock, category_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
            (product.name, product.description, product.price, product.stock, product.category_id)
        )
        db.commit()
        
        last_id = cursor.lastrowid
        cursor.execute("SELECT * FROM products WHERE id = ?", (last_id,))
        row = cursor.fetchone()
        db.close()
        return {"id": row[0], "name": row[1], "description": row[2], "price": row[3], 
                "stock": row[4], "category_id": row[5], "created_at": row[6], "updated_at": row[7]}
    except Exception as e:
        db.close()
        raise HTTPException(status_code=500, detail="Ürün oluşturma hatası")

@router.patch("/{product_id}", summary="Ürün bilgilerini güncelle")
def update_product(product_id: int, product_update: ProductUpdate):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    if not cursor.fetchone():
        db.close()
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    
    if product_update.category_id is not None:
        cursor.execute("SELECT * FROM categories WHERE id = ?", (product_update.category_id,))
        if not cursor.fetchone():
            db.close()
            raise HTTPException(status_code=400, detail="Geçersiz kategori ID'si")
    
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    current = cursor.fetchone()
    
    if product_update.name is not None:
        final_name = product_update.name
    else:
        final_name = current[1]
    
    if product_update.description is not None:
        final_description = product_update.description
    else:
        final_description = current[2]
    
    if product_update.price is not None:
        final_price = product_update.price
    else:
        final_price = current[3]
    
    if product_update.stock is not None:
        final_stock = product_update.stock
    else:
        final_stock = current[4]
    
    if product_update.category_id is not None:
        final_category_id = product_update.category_id
    else:
        final_category_id = current[5]
    
    try:
        cursor.execute(
            "UPDATE products SET name=?, description=?, price=?, stock=?, category_id=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (final_name, final_description, final_price, final_stock, final_category_id, product_id)
        )
        db.commit()
        
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        db.close()
        return {"id": row[0], "name": row[1], "description": row[2], "price": row[3], 
                "stock": row[4], "category_id": row[5], "created_at": row[6], "updated_at": row[7]}
    except Exception as e:
        db.close()
        raise HTTPException(status_code=400, detail="Güncelleme hatası")

@router.delete("/{product_id}", summary="Ürünü sil")
def delete_product(product_id: int):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    if not cursor.fetchone():
        db.close()
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    
    try:
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        db.commit()
        db.close()
        return {"message": "Ürün başarıyla silindi"}
    except Exception as e:
        db.close()
        raise HTTPException(status_code=400, detail="Silme hatası")
