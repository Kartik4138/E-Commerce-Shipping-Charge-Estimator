from sqlalchemy import select
from app.models import Warehouse, WarehouseInventory
from app.utils.distance import haversine


async def get_nearest_warehouse(
    db,
    seller,
    product_id,
    quantity
):
    result = await db.execute(select(Warehouse))
    warehouses = result.scalars().all()

    valid = []

    for wh in warehouses:
        inventory = (
            await db.execute(
                select(WarehouseInventory).where(
                    WarehouseInventory.warehouse_id == wh.id,
                    WarehouseInventory.product_id == product_id
                )
            )
        ).scalar_one_or_none()

        if not inventory:
            continue

        if inventory.available_units < quantity:
            continue

        if wh.capacity < quantity:
            continue

        distance = haversine(
            seller.latitude,
            seller.longitude,
            wh.latitude,
            wh.longitude
        )

        valid.append((wh, distance))

    if not valid:
        raise Exception("No warehouse available with sufficient stock.")

    valid.sort(key=lambda x: x[1])
    return valid[0][0]
