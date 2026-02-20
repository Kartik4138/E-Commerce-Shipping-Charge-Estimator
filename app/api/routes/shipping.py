from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Warehouse, Customer, Product
from app.schemas import ShippingRequest
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
    """ Calculates shipping charge from a specific warehouse to a customer. 
    Flow: 1. Check Redis cache. 
    2. Validate warehouse, customer, and product existence. 
    3. Calculate geographic distance using Haversine formula. 
    4. Select transport strategy dynamically. 
    5. Compute shipping cost. 
    6. Cache and return response. 
    """

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

        actual_weight = product.weight * quantity
        volumetric_weight = (
            (product.length * product.width * product.height) / 5000
        ) * quantity

        final_weight = max(actual_weight, volumetric_weight)

        strategy, _ = transport_factory(distance, deliverySpeed)

        base_cost = await strategy.calculate(distance, final_weight)

        courier_charge = 10
        express_charge = 0

        if deliverySpeed == "express":
            express_charge = 1.2 * final_weight

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
    request: ShippingRequest,
    db: AsyncSession = Depends(get_db)
):
    """ Aggregator endpoint: 
    1. Finds nearest warehouse for seller. 
    2. Calculates shipping charge. 
    3. Returns combined structured response. Delegates core business logic to service layer. 
    """

    cache_key = (
        f"combined:{request.sellerId}:{request.customerId}:"
        f"{request.productId}:{request.quantity}:"
        f"{request.deliverySpeed}"
    )

    cached_response = await get_cached_data(cache_key)
    if cached_response:
        return cached_response

    try:
        result = await calculate_shipping(
            db,
            request.sellerId,
            request.customerId,
            request.productId,
            request.quantity,
            request.deliverySpeed
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
