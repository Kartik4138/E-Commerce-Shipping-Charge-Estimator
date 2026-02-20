import pytest
from app.services.transport_strategy import transport_factory


@pytest.mark.asyncio
async def test_minivan_selection():
    strategy, mode = transport_factory(50, "standard")
    assert mode == "Mini Van"


@pytest.mark.asyncio
async def test_truck_selection():
    strategy, mode = transport_factory(200, "standard")
    assert mode == "Truck"


@pytest.mark.asyncio
async def test_airplane_override_express():
    strategy, mode = transport_factory(400, "express")
    assert mode == "Aeroplane"
