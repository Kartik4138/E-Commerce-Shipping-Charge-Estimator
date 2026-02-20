from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Warehouse, Customer, Product
from app.services.shipping_service import calculate_shipping
from app.api.deps import get_db
from app.cache import get_cached_data, set_cached_data
from app.utils.distance import haversine
from app.services.transport_strategy import transport_factory

router = APIRouter(
    prefix="/shipping-charge",
    tags=["Shipping"]
)

@router.get("")
async def get_shipping_charge(
    warehouseId: int = Query(...),
    customerId: int = Query(...),
    productId: int = Query(...),
    quantity: int = Query(1),
    deliverySpeed: str = Query(...),
    db: AsyncSession = Depends(get_db)
):

    cache_key = f"shipping:{warehouseId}:{customerId}:{productId}:{quantity}:{deliverySpeed}"

    cached_response = await get_cached_data(cache_key)
    if cached_response:
        return cached_response

    try:
        warehouse = (
            await db.execute(
                select(Warehouse).where(Warehouse.id == warehouseId)
            )
        ).scalar_one_or_none()

        if not warehouse:
            raise HTTPException(status_code=404, detail="Warehouse not found")

        customer = (
            await db.execute(
                select(Customer).where(Customer.id == customerId)
            )
        ).scalar_one_or_none()

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        product = (
            await db.execute(
                select(Product).where(Product.id == productId)
            )
        ).scalar_one_or_none()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        distance = haversine(
            warehouse.latitude,
            warehouse.longitude,
            customer.latitude,
            customer.longitude
        )

        total_weight = product.weight * quantity

        strategy, _ = transport_factory(distance, deliverySpeed)

        base_cost = await strategy.calculate(distance, total_weight)

        courier_charge = 10
        express_charge = 0

        if deliverySpeed == "express":
            express_charge = 1.2 * total_weight

        final_cost = base_cost + courier_charge + express_charge

        response = {
            "shippingCharge": round(final_cost, 2)
        }

        await set_cached_data(cache_key, response)

        return response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/calculate")
async def calculate_combined(
    request: dict,
    db: AsyncSession = Depends(get_db)
):

    cache_key = (
        f"combined:{request['sellerId']}:{request['customerId']}:"
        f"{request['productId']}:{request.get('quantity',1)}:"
        f"{request['deliverySpeed']}"
    )

    cached_response = await get_cached_data(cache_key)
    if cached_response:
        return cached_response

    try:
        result = await calculate_shipping(
            db,
            request["sellerId"],
            request["customerId"],
            request["productId"],
            request.get("quantity", 1),
            request["deliverySpeed"]
        )

        response = {
            "shippingCharge": result["finalCost"],
            "nearestWarehouse": {
                "warehouseId": result.get("warehouseId"),
                "warehouseLocation": result.get("warehouseLocation")
            }
        }

        await set_cached_data(cache_key, response)

        return response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
