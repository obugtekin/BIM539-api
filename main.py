from fastapi import FastAPI
from database import init_db
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
            "documentation": "/api-docs"
        }
    }

app.include_router(users_router.router, prefix="/api/users", tags=["Users"])
app.include_router(categories_router.router, prefix="/api/categories", tags=["Categories"])
app.include_router(products_router.router, prefix="/api/products", tags=["Products"])
app.include_router(orders_router.router, prefix="/api/orders", tags=["Orders"])
app.include_router(reviews_router.router, prefix="/api/reviews", tags=["Reviews"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
