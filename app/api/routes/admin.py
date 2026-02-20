from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.api.deps import get_db
from app.models import Seller, Customer, Warehouse, Product, WarehouseInventory
from app.schemas import (
    SellerCreate,
    CustomerCreate,
    WarehouseCreate,
    ProductCreate,
    InventoryCreate,
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin Data Entry"]
)


# Add Seller
@router.post("/seller")
async def add_seller(
    payload: SellerCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        seller = Seller(**payload.model_dump())
        db.add(seller)
        await db.commit()
        await db.refresh(seller)
        return seller

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Duplicate or invalid seller data")

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Add Customer
@router.post("/customer")
async def add_customer(
    payload: CustomerCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        customer = Customer(**payload.model_dump())
        db.add(customer)
        await db.commit()
        await db.refresh(customer)
        return customer

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Duplicate or invalid customer data")

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Add Warehouse
@router.post("/warehouse")
async def add_warehouse(
    payload: WarehouseCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        warehouse = Warehouse(**payload.model_dump())
        db.add(warehouse)
        await db.commit()
        await db.refresh(warehouse)
        return warehouse

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Invalid warehouse data")

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Add Product
@router.post("/product")
async def add_product(
    payload: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        product = Product(**payload.model_dump())
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Invalid product data")

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


#  Add Inventory
@router.post("/inventory")
async def add_inventory(
    payload: InventoryCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        inventory = WarehouseInventory(**payload.model_dump())
        db.add(inventory)
        await db.commit()
        await db.refresh(inventory)
        return inventory

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Invalid inventory data")

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
