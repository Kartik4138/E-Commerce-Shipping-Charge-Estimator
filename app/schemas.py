from pydantic import BaseModel


class ShippingRequest(BaseModel):
    sellerId: int
    customerId: int
    productId: int
    quantity: int
    deliverySpeed: str


class ShippingResponse(BaseModel):
    distance: float
    transportMode: str
    baseCost: float
    courierCharge: float
    expressCharge: float
    finalCost: float
    estimatedDays: int
