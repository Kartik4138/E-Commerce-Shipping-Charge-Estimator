from sqlalchemy import select
from app.models import Seller, Customer, Product
from app.services.transport_strategy import transport_factory
from app.services.warehouse_service import get_nearest_warehouse
from app.utils.distance import haversine

MAX_SERVICE_DISTANCE = 2000


async def calculate_shipping(
    db,
    seller_id,
    customer_id,
    product_id,
    quantity,
    delivery_speed
):

    seller = (await db.execute(
        select(Seller).where(Seller.id == seller_id)
    )).scalar_one_or_none()

    if not seller:
        raise Exception("Seller not found")

    customer = (await db.execute(
        select(Customer).where(Customer.id == customer_id)
    )).scalar_one_or_none()

    if not customer:
        raise Exception("Customer not found")

    product = (await db.execute(
        select(Product).where(Product.id == product_id)
    )).scalar_one_or_none()

    if not product:
        raise Exception("Product not found")

    warehouse = await get_nearest_warehouse(
        db,
        seller,
        product_id,
        quantity
    )

    distance = haversine(
        warehouse.latitude,
        warehouse.longitude,
        customer.latitude,
        customer.longitude
    )

    if distance > MAX_SERVICE_DISTANCE:
        raise Exception("Delivery location not supported.")

    actual_weight = product.weight * quantity
    volumetric_weight = (
        (product.length * product.width * product.height) / 5000
    ) * quantity

    final_weight = max(actual_weight, volumetric_weight)

    strategy, mode = transport_factory(distance, delivery_speed)

    base_cost = await strategy.calculate(distance, final_weight)

    courier_charge = 10
    express_charge = 0

    if delivery_speed == "express":
        express_charge = 1.2 * final_weight

    final_cost = base_cost + courier_charge + express_charge
    
    return {
        "warehouseId": warehouse.id,
        "warehouseLocation": {
            "lat": warehouse.latitude,
            "long": warehouse.longitude
        },
        "distance": round(distance, 2),
        "transportMode": mode,
        "baseCost": round(base_cost, 2),
        "courierCharge": courier_charge,
        "expressCharge": round(express_charge, 2),
        "finalCost": round(final_cost, 2),
        "estimatedDays": strategy.eta()
    }
