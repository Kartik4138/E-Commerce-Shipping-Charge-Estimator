import pytest


@pytest.mark.asyncio
async def test_missing_params(client):
    response = await client.get("/api/v1/shipping-charge")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_invalid_warehouse(client):
    response = await client.get(
        "/api/v1/shipping-charge",
        params={
            "warehouseId": 999,
            "customerId": 1,
            "productId": 1,
            "quantity": 1,
            "deliverySpeed": "standard"
        }
    )
    assert response.status_code == 404
