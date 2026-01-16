from fastapi import FastAPI, HTTPException
from database import init_db, get_db
import routers.users as users_router
import routers.categories as categories_router
import routers.products as products_router
import routers.orders as orders_router
import routers.reviews as reviews_router

app = FastAPI(
    title="REST API Projesi",
    description="Yazılım Kalite Güvencesi ve Testi Dönem Sonu Projesi",
    version="1.0.0",
    docs_url="/api-docs"
)

init_db()

@app.get("/")
def root():
    return {
        "message": "REST API Projesi - Yazılım Kalite Güvencesi ve Testi",
        "version": "1.0.0",
        "endpoints": {
            "users": "/api/users",
            "categories": "/api/categories",
            "products": "/api/products",
            "orders": "/api/orders",
            "reviews": "/api/reviews",
            "documentation": "/api-docs",
            "health": "/api/health"
        }
    }

@app.get("/api/health")
def health_check():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        db.close()
        return {
            "status": "ok",
            "database": "connected"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

app.include_router(users_router.router, prefix="/api/users", tags=["Users"])
app.include_router(categories_router.router, prefix="/api/categories", tags=["Categories"])
app.include_router(products_router.router, prefix="/api/products", tags=["Products"])
app.include_router(orders_router.router, prefix="/api/orders", tags=["Orders"])
app.include_router(reviews_router.router, prefix="/api/reviews", tags=["Reviews"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
