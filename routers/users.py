from fastapi import APIRouter, HTTPException
from database import get_db
from models import User, UserCreate, UserUpdate
import sqlite3

router = APIRouter()

@router.get("/", summary="Tüm kullanıcıları listele")
def get_users():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    db.close()
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "phone": row[3],
            "created_at": row[4],
            "updated_at": row[5]
        })
    return result

@router.get("/{user_id}", summary="ID'ye göre kullanıcı getir")
def get_user(user_id: int):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    db.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    return {"id": row[0], "name": row[1], "email": row[2], "phone": row[3], 
            "created_at": row[4], "updated_at": row[5]}

@router.post("/", status_code=201, summary="Yeni kullanıcı oluştur")
def create_user(user: UserCreate):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (name, email, phone, created_at, updated_at) VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
            (user.name, user.email, user.phone)
        )
        db.commit()
        
        last_id = cursor.lastrowid
        cursor.execute("SELECT * FROM users WHERE id = ?", (last_id,))
        row = cursor.fetchone()
        db.close()
        return {"id": row[0], "name": row[1], "email": row[2], "phone": row[3], 
                "created_at": row[4], "updated_at": row[5]}
    except Exception as e:
        db.close()
        raise HTTPException(status_code=400, detail="Kullanıcı oluşturma hatası")

@router.patch("/{user_id}", summary="Kullanıcı bilgilerini güncelle")
def update_user(user_id: int, user_update: UserUpdate):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    current = cursor.fetchone()
    if not current:
        db.close()
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    if user_update.name is not None:
        name = user_update.name
    else:
        name = current[1]
    
    if user_update.email is not None:
        email = user_update.email
    else:
        email = current[2]
    
    if user_update.phone is not None:
        phone = user_update.phone
    else:
        phone = current[3]
    
    try:
        cursor.execute(
            "UPDATE users SET name=?, email=?, phone=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (name, email, phone, user_id)
        )
        db.commit()
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        db.close()
        return {"id": row[0], "name": row[1], "email": row[2], "phone": row[3], 
                "created_at": row[4], "updated_at": row[5]}
    except Exception as e:
        db.close()
        raise HTTPException(status_code=400, detail="Güncelleme hatası")

@router.delete("/{user_id}", summary="Kullanıcıyı sil")
def delete_user(user_id: int):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    if not cursor.fetchone():
        db.close()
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        db.commit()
        db.close()
        return {"message": "Kullanıcı başarıyla silindi"}
    except Exception as e:
        db.close()
        raise HTTPException(status_code=400, detail="Silme hatası")
