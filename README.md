# REST API Projesi

Yazılım Kalite Güvencesi ve Testi Dönem Sonu Projesi

## Proje Hakkında

Bu ödev, en az 5 farklı kaynak içeren bir REST API uygulamasıdır. API, kullanıcılar, kategoriler, ürünler, siparişler ve yorumlar gibi kaynakları yönetmek için tasarlanmıştır.

## Kullanılan Teknolojiler

- Python + FastAPI
- SQLite veritabanı
- Swagger/OpenAPI dokümantasyonu
- pytest

## Proje Yapısı

```
api_new/
├── routers/          
│   ├── users.py
│   ├── categories.py
│   ├── products.py
│   ├── orders.py
│   └── reviews.py
├── database.py       
├── models.py         
├── main.py           
├── requirements.txt  
└── README.md         
```

## Kurulum Talimatları

### 1. Gereksinimler

- Python 3.8 veya üzeri
- pip 

### 2. Adımlar

1. Projeyi klonlayın veya indirin:
```bash
git clone <repository-url>
cd api_new
```

2. Requirementsları yükleyin:
```bash
pip install -r requirements.txt
```

3. Sunucuyu başlatın:
```bash
uvicorn main:app --reload
```

4. Sunucu çalıştığında:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

## API Endpoint'leri

### Base URL
```
http://localhost:8000
```

### Kaynaklar ve Endpoint'ler

#### 1. Users 
- `GET /api/users` - 
- `GET /api/users/{user_id}` - 
- `POST /api/users` - 
- `PATCH /api/users/{user_id}` - 
- `DELETE /api/users/{user_id}` - 

#### 2. Categories
- `GET /api/categories` 
- `GET /api/categories/{category_id}`  
- `POST /api/categories`
- `PATCH /api/categories/{category_id}` 
- `DELETE /api/categories/{category_id}` 

#### 3. Products 
- `GET /api/products` - 
- `GET /api/products/{product_id}` - 
- `POST /api/products` 
- `PATCH /api/products/{product_id}` 
- `DELETE /api/products/{product_id}` 

#### 4. Orders 
- `GET /api/orders` 
- `GET /api/orders/{order_id}` 
- `POST /api/orders` 
- `PATCH /api/orders/{order_id}` 
- `DELETE /api/orders/{order_id}`

#### 5. Reviews 
- `GET /api/reviews`
- `GET /api/reviews/{review_id}` 
- `POST /api/reviews` 
- `PATCH /api/reviews/{review_id}` 
- `DELETE /api/reviews/{review_id}` 

## API Kullanım Örnekleri

### 1. Yeni Kullanıcı Oluşturma

```bash
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ONUR BUĞTEKİN",
    "email": "onurbugtekin@example.com",
    "phone": "555-555 5555"
  }'
```

**Response (201 Created):**
```json
{
  "id": 3,
  "name": "ONUR BUĞTEKİN",
  "email": "onurbugtekin@example.com",
  "phone": "555-555 5555",
  "created_at": "2026-01-10 10:30:00",
  "updated_at": "2026-01-10 10:30:00"
}
```

### 2. Tüm Ürünleri Listeleme

```bash
curl http://localhost:8000/api/products
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "description": "RTX 4060 laptop",
    "price": 15000.00,
    "stock": 10,
    "category_id": 1,
    "category_name": "Elektronik",
    "created_at": "2026-01-10 10:00:00",
    "updated_at": "2026-01-10 10:00:00"
  }
]
```

### 3. Ürün Güncelleme

```bash
curl -X PATCH http://localhost:8000/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "price": 14000.00,
    "stock": 15
  }'
```

### 4. Sipariş Oluşturma

```bash
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "total_amount": 15000.00,
    "status": "pending"
  }'
```

### 5. Yorum Oluşturma

```bash
curl -X POST http://localhost:8000/api/reviews \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "product_id": 1,
    "rating": 5,
    "comment": "Harika bir ürün, çok memnun kaldım!"
  }'
```

## Veritabanı İlişkileri

- **Users ↔ Orders**: Bir kullanıcının birden fazla siparişi olabilir (1-N)
- **Categories ↔ Products**: Bir kategorinin birden fazla ürünü olabilir (1-N)
- **Users ↔ Reviews**: Bir kullanıcının birden fazla yorumu olabilir (1-N)
- **Products ↔ Reviews**: Bir ürünün birden fazla yorumu olabilir (1-N)

## HTTP Durum Kodları

- `200 OK`: İstek başarılı
- `201 Created`: Yeni kaynak başarıyla oluşturuldu
- `400 Bad Request`: Geçersiz istek (validasyon hatası vb.)
- `404 Not Found`: Kaynak bulunamadı
- `500 Internal Server Error`: Sunucu hatası

## Swagger Dokümantasyonu

API dokümantasyonu:

```
http://localhost:8000/api-docs
```

## Test Çalıştırma

Testleri çalıştırmak için:

```bash
# Tüm testleri çalıştır
pytest

# Coverage raporu ile
pytest --cov=.

# Sadece birim testler
pytest tests/test_models.py tests/test_validation.py

# Sadece entegrasyon testleri
pytest tests/test_integration.py tests/test_categories_basic.py

# Sadece sistem testleri
pytest tests/test_system.py
```

## Notlar

- Veritabanı dosyası otomatik oluşturulur
- İlk çalıştırmada örnek veriler eklenir
- Email adresleri ve kategori isimleri benzersiz olmalı




