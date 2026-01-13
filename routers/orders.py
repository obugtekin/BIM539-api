from fastapi import APIRouter, HTTPException
from database import get_db
from models import Order, OrderCreate, OrderUpdate
import sqlite3

router = APIRouter()

@router.get("/", summary="Tüm siparişleri listele")
def get_orders():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    db.close()
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "user_id": row[1],
            "total_amount": row[2],
            "status": row[3],
            "order_date": row[4]
        })
    return result

@router.get("/{order_id}", summary="ID'ye göre sipariş getir")
def get_order(order_id: int):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    row = cursor.fetchone()
    db.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
    
    return {"id": row[0], "user_id": row[1], "total_amount": row[2], 
            "status": row[3], "order_date": row[4]}

@router.post("/", status_code=201, summary="Yeni sipariş oluştur")
def create_order(order: OrderCreate):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (order.user_id,))
    if not cursor.fetchone():
        db.close()
        raise HTTPException(status_code=400, detail="Geçersiz kullanıcı ID'si")
    
    try:
        cursor.execute(
            "INSERT INTO orders (user_id, total_amount, status, order_date) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
            (order.user_id, order.total_amount, order.status)
        )
        db.commit()
        
        last_id = cursor.lastrowid
        cursor.execute("SELECT * FROM orders WHERE id = ?", (last_id,))
        row = cursor.fetchone()
        db.close()
        return {"id": row[0], "user_id": row[1], "total_amount": row[2], 
                "status": row[3], "order_date": row[4]}
    except Exception as e:
        db.close()
        raise HTTPException(status_code=500, detail="Sipariş oluşturma hatası")

@router.patch("/{order_id}", summary="Sipariş bilgilerini güncelle")
def update_order(order_id: int, order_update: OrderUpdate):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    current = cursor.fetchone()
    if not current:
        db.close()
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
    
    if order_update.user_id is not None:
        cursor.execute("SELECT * FROM users WHERE id = ?", (order_update.user_id,))
        if not cursor.fetchone():
            db.close()
            raise HTTPException(status_code=400, detail="Geçersiz kullanıcı ID'si")
        user_id = order_update.user_id
    else:
        user_id = current[1]
    
    if order_update.total_amount is not None:
        total_amount = order_update.total_amount
    else:
        total_amount = current[2]
    
    if order_update.status is not None:
        status = order_update.status
    else:
        status = current[3]
    
    try:
        cursor.execute(
            "UPDATE orders SET user_id=?, total_amount=?, status=? WHERE id=?",
            (user_id, total_amount, status, order_id)
        )
        db.commit()
        
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        db.close()
        return {"id": row[0], "user_id": row[1], "total_amount": row[2], 
                "status": row[3], "order_date": row[4]}
    except Exception as e:
        db.close()
        raise HTTPException(status_code=400, detail="Güncelleme hatası")

@router.delete("/{order_id}", summary="Siparişi sil")
def delete_order(order_id: int):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    if not cursor.fetchone():
        db.close()
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
    
    try:
        cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        db.commit()
        db.close()
        return {"message": "Sipariş başarıyla silindi"}
    except Exception as e:
        db.close()
        raise HTTPException(status_code=400, detail="Silme hatası")
