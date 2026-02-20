from pydantic import BaseModel, Field


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


class SellerBase(BaseModel):
    name: str = Field(..., min_length=2)
    latitude: float
    longitude: float


class SellerCreate(SellerBase):
    pass


class SellerResponse(SellerBase):
    id: int

    class Config:
        from_attributes = True


class CustomerBase(BaseModel):
    name: str = Field(..., min_length=2)
    latitude: float
    longitude: float


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    id: int

    class Config:
        from_attributes = True


class WarehouseBase(BaseModel):
    name: str = Field(..., min_length=2)
    latitude: float
    longitude: float
    capacity: int = Field(..., gt=0)


class WarehouseCreate(WarehouseBase):
    pass


class WarehouseResponse(WarehouseBase):
    id: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    seller_id: int
    name: str = Field(..., min_length=2)
    weight: float = Field(..., gt=0)
    length: float = Field(..., gt=0)
    width: float = Field(..., gt=0)
    height: float = Field(..., gt=0)


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True


class InventoryBase(BaseModel):
    warehouse_id: int
    product_id: int
    available_units: int = Field(..., ge=0)


class InventoryCreate(InventoryBase):
    pass


class InventoryResponse(InventoryBase):
    id: int

    class Config:
        from_attributes = True
