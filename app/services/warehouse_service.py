from sqlalchemy import select
from app.models import Warehouse, WarehouseInventory
from app.utils.distance import haversine
from fastapi import HTTPException


async def get_nearest_warehouse(db, seller, product_id, quantity):

    warehouses = (await db.execute(
        select(Warehouse)
    )).scalars().all()

    eligible_warehouses = []

    for warehouse in warehouses:

        # Check inventory for this warehouse + product
        inventory = (await db.execute(
            select(WarehouseInventory).where(
                WarehouseInventory.warehouse_id == warehouse.id,
                WarehouseInventory.product_id == product_id
            )
        )).scalar_one_or_none()

        # Skip if no inventory or insufficient stock
        if not inventory or inventory.available_units < quantity:
            continue

        distance = haversine(
            seller.latitude,
            seller.longitude,
            warehouse.latitude,
            warehouse.longitude
        )

        eligible_warehouses.append((warehouse, distance))

    if not eligible_warehouses:
        raise HTTPException(
            status_code=400,
            detail="No warehouse available with sufficient stock."
        )

    eligible_warehouses.sort(key=lambda x: x[1])

    return eligible_warehouses[0][0]
