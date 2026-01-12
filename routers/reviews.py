from fastapi import APIRouter, HTTPException
from database import get_db
from models import Review, ReviewCreate, ReviewUpdate
import sqlite3

router = APIRouter()

@router.get("/", summary="Tüm yorumları listele")
def get_reviews():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM reviews")
    rows = cursor.fetchall()
    db.close()
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "user_id": row[1],
            "product_id": row[2],
            "rating": row[3],
            "comment": row[4],
            "created_at": row[5]
        })
    return result

@router.get("/{review_id}", summary="ID'ye göre yorum getir")
def get_review(review_id: int):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM reviews WHERE id = ?", (review_id,))
    row = cursor.fetchone()
    db.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Yorum bulunamadı")
    
    return {"id": row[0], "user_id": row[1], "product_id": row[2], 
            "rating": row[3], "comment": row[4], "created_at": row[5]}

@router.post("/", status_code=201, summary="Yeni yorum oluştur")
def create_review(review: ReviewCreate):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (review.user_id,))
    if not cursor.fetchone():
        db.close()
        raise HTTPException(status_code=400, detail="Geçersiz kullanıcı ID'si")
    
    cursor.execute("SELECT * FROM products WHERE id = ?", (review.product_id,))
    if not cursor.fetchone():
        db.close()
        raise HTTPException(status_code=400, detail="Geçersiz ürün ID'si")
    
    try:
        cursor.execute(
            "INSERT INTO reviews (user_id, product_id, rating, comment, created_at) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)",
            (review.user_id, review.product_id, review.rating, review.comment)
        )
        db.commit()
        
        last_id = cursor.lastrowid
        cursor.execute("SELECT * FROM reviews WHERE id = ?", (last_id,))
        row = cursor.fetchone()
        db.close()
        return {"id": row[0], "user_id": row[1], "product_id": row[2], 
                "rating": row[3], "comment": row[4], "created_at": row[5]}
    except Exception as e:
        db.close()
        raise HTTPException(status_code=500, detail="Yorum oluşturma hatası")

@router.patch("/{review_id}", summary="Yorum bilgilerini güncelle")
def update_review(review_id: int, review_update: ReviewUpdate):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM reviews WHERE id = ?", (review_id,))
    current = cursor.fetchone()
    if not current:
        db.close()
        raise HTTPException(status_code=404, detail="Yorum bulunamadı")
    
    if review_update.rating is not None:
        rating = review_update.rating
    else:
        rating = current[3]
    
    if review_update.comment is not None:
        comment = review_update.comment
    else:
        comment = current[4]
    
    cursor.execute(
        "UPDATE reviews SET rating=?, comment=? WHERE id=?",
        (rating, comment, review_id)
    )
    db.commit()
    
    cursor.execute("SELECT * FROM reviews WHERE id = ?", (review_id,))
    row = cursor.fetchone()
    db.close()
    return {"id": row[0], "user_id": row[1], "product_id": row[2], 
            "rating": row[3], "comment": row[4], "created_at": row[5]}

@router.delete("/{review_id}", summary="Yorumu sil")
def delete_review(review_id: int):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM reviews WHERE id = ?", (review_id,))
    if not cursor.fetchone():
        db.close()
        raise HTTPException(status_code=404, detail="Yorum bulunamadı")
    
    cursor.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
    db.commit()
    db.close()
    
    return {"message": "Yorum başarıyla silindi"}
