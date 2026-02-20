# 🚚 B2B E-Commerce Shipping Charge Estimator

A high-performance, asynchronous REST API built with **FastAPI** to calculate shipping charges for a B2B e-commerce marketplace.

This system connects **Kirana stores (customers)** with **sellers**, dynamically determines the nearest warehouse, validates inventory constraints, and calculates optimized shipping charges based on:

- 📍 Distance (Haversine formula)
- 🚛 Transport strategy (MiniVan, Truck, Airplane)
- 📦 Volumetric weight logic
- ⚡ Delivery speed (Standard / Express)

---

## ⚡ Key Features

### 🗺️ Intelligent Warehouse Routing
- Uses the Haversine formula for geospatial distance calculation.
- Filters warehouses by inventory availability.
- Selects the nearest eligible warehouse.

### 💰 Smart Shipping Engine
- Strategy Pattern for transport mode selection:
  - MiniVan (short distance)
  - Truck (medium distance)
  - Airplane (long distance)
- Supports Standard and Express delivery pricing.
- Applies volumetric weight pricing logic.

### 📦 Volumetric Weight Handling
Shipping cost is calculated using:

```
Chargeable Weight = max(actual_weight, volumetric_weight)
```

Where:

```
volumetric_weight = (length × width × height) / 5000
```

### ⚡ High Performance Architecture
- Fully asynchronous FastAPI application
- Async SQLAlchemy + asyncpg
- Redis caching with smart invalidation
- Dockerized infrastructure

### 🏬 Inventory-Aware Routing
- Validates stock before routing
- Automatically falls back to farther warehouse if nearest is out of stock
- Prevents invalid shipments

---

# 🛠️ Tech Stack

| Layer | Technology |
|--------|------------|
| Framework | FastAPI |
| Language | Python 3.10+ |
| Database | PostgreSQL |
| ORM | SQLAlchemy (Async) |
| Driver | asyncpg |
| Caching | Redis |
| Validation | Pydantic |
| Testing | Pytest |
| Containerization | Docker & Docker Compose |

---

# 📦 Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone <your-repo-url>
cd shipping-estimator
```

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Configure Environment Variables

Set:

```
DATABASE_URL=postgresql+asyncpg://<user>:<password>@<host>/<dbname>
REDIS_HOST=localhost
```

Ensure:
- PostgreSQL is running
- Redis is running on `localhost:6379`

## 5️⃣ Run Application

```bash
uvicorn app.main:app --reload
```

Access:
- API → http://localhost:8000
- Swagger Docs → http://localhost:8000/docs

## 6️⃣ Run Tests

```bash
pytest -v
```

If running Redis via Docker:

```bash
$env:REDIS_HOST="localhost"; pytest -v
```

---

# 🐳 Docker Setup

The application runs with:

- FastAPI (Uvicorn)
- PostgreSQL
- Redis

## Build and Start

```bash
docker-compose up --build
```

Run in background:

```bash
docker-compose up -d --build
```

## Access

- API → http://localhost:8000
- Swagger Docs → http://localhost:8000/docs
- PostgreSQL → localhost:5432
- Redis → localhost:6379

## Stop

```bash
docker-compose down
```

Remove volumes:

```bash
docker-compose down -v
```

---

# 📖 API Documentation

---

# 🧑‍💼 Admin APIs

Base Route:

```
/api/v1/admin
```

---

## ➤ Add Seller

**POST** `/api/v1/admin/seller`

```json
{
  "name": "Nestle Seller",
  "latitude": 12.9716,
  "longitude": 77.5946
}
```

---

## ➤ Add Customer

**POST** `/api/v1/admin/customer`

```json
{
  "name": "Shree Kirana Store",
  "latitude": 13.0352,
  "longitude": 77.5970
}
```

---

## ➤ Add Warehouse

**POST** `/api/v1/admin/warehouse`

```json
{
  "name": "BLR_Warehouse",
  "latitude": 12.9762,
  "longitude": 77.6033,
  "capacity": 1000
}
```

---

## ➤ Add Product

**POST** `/api/v1/admin/product`

```json
{
  "seller_id": 1,
  "name": "Rice Bag 10kg",
  "weight": 10,
  "length": 100,
  "width": 50,
  "height": 40
}
```

---

## ➤ Add / Update Inventory (Upsert)

**POST** `/api/v1/admin/inventory`

```json
{
  "warehouse_id": 1,
  "product_id": 1,
  "available_units": 200
}
```

If inventory exists → updates  
If not → inserts new row  

Cache invalidation is triggered automatically.

---

# 🚚 Core Business APIs

---

## ➤ Get Nearest Warehouse

**GET** `/api/v1/warehouse/nearest`

Query Parameters:
- `sellerId`
- `productId`
- `quantity`

Response:

```json
{
  "warehouseId": 1,
  "warehouseLocation": {
    "lat": 12.9762,
    "long": 77.6033
  }
}
```

---

## ➤ Get Shipping Charge (Warehouse-Based)

**GET** `/api/v1/shipping-charge`

Query Parameters:
- `warehouseId`
- `customerId`
- `productId`
- `quantity`
- `deliverySpeed` ("standard" | "express")

---

## ➤ Combined Shipping Calculation (Recommended)

**POST** `/api/v1/shipping-charge/calculate`

```json
{
  "sellerId": 1,
  "customerId": 1,
  "productId": 1,
  "quantity": 5,
  "deliverySpeed": "express"
}
```

Response:

```json
{
  "shippingCharge": 245.50,
  "nearestWarehouse": {
    "warehouseId": 1,
    "warehouseLocation": {
      "lat": 12.9762,
      "long": 77.6033
    }
  }
}
```

---

# 🏗️ Architecture & Design Patterns

### Strategy Pattern
Used for transport pricing logic:
- MiniVanStrategy
- TruckStrategy
- AirplaneStrategy

### Factory Pattern
`transport_factory()` dynamically selects transport mode based on distance and delivery speed.

### Service Layer Architecture
- Routes remain thin
- Business logic handled in services
- Clean separation of concerns

---

# 🧪 Testing Coverage

- Distance calculation validation
- Volumetric weight logic
- Inventory validation
- Transport strategy selection
- API integration tests
- Cache invalidation behavior

---

# 🚀 Future Enhancements

- JWT Authentication
- Role-Based Access Control
- Order placement with inventory decrement
- Rate limiting
- CI/CD Pipeline
- Kubernetes deployment

---

# 👨‍💻 Author

Kartik Singh  
Backend & Systems Enthusiast
