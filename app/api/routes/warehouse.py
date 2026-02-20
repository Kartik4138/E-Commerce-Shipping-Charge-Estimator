from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Seller
from app.services.warehouse_service import get_nearest_warehouse
from app.api.deps import get_db

router = APIRouter(
    prefix="/warehouse",
    tags=["Warehouse"]
)


@router.get("/nearest")
async def nearest(
    sellerId: int,
    productId: int,
    quantity: int,
    db: AsyncSession = Depends(get_db)
):

    seller = (
        await db.execute(select(Seller).where(Seller.id == sellerId))
    ).scalar_one_or_none()

    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    try:
        warehouse = await get_nearest_warehouse(
            db,
            seller,
            productId,
            quantity
        )

        return {
            "warehouseId": warehouse.id,
            "warehouseLocation": {
                "lat": warehouse.latitude,
                "long": warehouse.longitude
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
