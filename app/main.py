from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routes import admin, shipping, warehouse
from app.database import engine, Base
import app.models 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables in the database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Async Logistics Pricing Engine",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(shipping.router, prefix="/api/v1")
app.include_router(warehouse.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")