from fastapi import FastAPI
from app.api.routes import shipping, warehouse

app = FastAPI(
    title="Async Logistics Pricing Engine",
    version="1.0.0"
)

app.include_router(shipping.router, prefix="/api/v1")
app.include_router(warehouse.router, prefix="/api/v1")
