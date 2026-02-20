# 🚚 B2B E-Commerce Shipping Charge Estimator

A high-performance, asynchronous REST API built with **FastAPI** to calculate shipping charges for a B2B e-commerce marketplace.

This system connects **Kirana stores (customers)** with **sellers**, dynamically determines the nearest drop-off warehouse, validates inventory constraints, and calculates optimized shipping charges based on distance, transport strategy, volumetric weight, and delivery speed.

---

## ⚡ Key Features

### 🗺️ Intelligent Warehouse Routing
- Uses the **Haversine Formula** to calculate geographic distance.
- Automatically selects the nearest warehouse with available inventory and capacity.

### 💰 Smart Shipping Engine
- Implements the **Strategy Pattern** to dynamically choose:
  - Mini Van (Short Distance)
  - Truck (Medium Distance)
  - Airplane (Long Distance)
- Supports **Standard** and **Express** delivery modes.

### ⚡ High Performance
- Fully asynchronous architecture using:
  - FastAPI
  - SQLAlchemy (Async)
  - asyncpg
- Redis caching for complex shipping calculations.

### 🏬 Inventory-Aware Routing
- Validates:
  - Warehouse stock availability
  - Capacity constraints
  - Seller-product mapping

### 🛠️ Admin Data Management APIs
- Create sellers
- Create customers
- Add warehouses
- Add products
- Manage warehouse inventory

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

Update your database connection:

```python
DATABASE_URL = "postgresql+asyncpg://<user>:<password>@<host>/<dbname>"
```

Ensure:
- PostgreSQL is running
- Redis is running on `localhost:6379`

## 5️⃣ Run Application

```bash
uvicorn app.main:app --reload
```

Access:
- API → `http://localhost:8000`
- Swagger Docs → `http://localhost:8000/docs`

## 6️⃣ Run Tests

```bash
pytest -v
```
or when using docker
```bash
$env:REDIS_HOST="localhost"; pytest -v
```

---

---

# 🐳 Docker Setup

This project is fully containerized using Docker and Docker Compose.

It runs:
- FastAPI (Uvicorn)
- PostgreSQL
- Redis

---

## 📦 Run the Application

### Build and start containers

```bash
docker-compose up --build
```

### Run in detached mode

```bash
docker-compose up -d --build
```

---

## 🌍 Access the Services

- API → http://localhost:8000
- Swagger Docs → http://localhost:8000/docs
- PostgreSQL → localhost:5432
- Redis → localhost:6379

---

## 🛑 Stop Containers

```bash
docker-compose down
```

To remove volumes:

```bash
docker-compose down -v
```

---

## ⚙️ Environment Configuration

Database connection is configured inside `docker-compose.yml`:

```
DATABASE_URL=postgresql+asyncpg://postgres:root@db:5432/shipping
```

---

## 🚀 Notes

- Uvicorn is used as the ASGI server.
- Containers communicate internally using service names (`db`, `redis`).
- No additional production server (e.g., Gunicorn) is used.

---


# 📖 API Documentation

---

# 🧑‍💼 Admin APIs

Base Route:

```
/admin
```

---

## ➤ Add Seller

**POST** `/admin/seller`

### Request Body
```json
{
  "name": "ABC Traders",
  "lat": 28.6139,
  "long": 77.2090
}
```

---

## ➤ Add Customer

**POST** `/admin/customer`

### Request Body
```json
{
  "name": "Kirana Store 1",
  "lat": 28.7041,
  "long": 77.1025
}
```

---

## ➤ Add Warehouse

**POST** `/admin/warehouse`

### Request Body
```json
{
  "name": "Delhi Central Warehouse",
  "lat": 28.5355,
  "long": 77.3910,
  "capacity": 10000
}
```

---

## ➤ Add Product

**POST** `/admin/product`

### Request Body
```json
{
  "name": "Rice 25kg",
  "weight": 25,
  "length": 50,
  "width": 40,
  "height": 20
}
```

---

## ➤ Add Inventory

**POST** `/admin/inventory`

### Request Body
```json
{
  "warehouseId": 1,
  "productId": 1,
  "availableQuantity": 500
}
```

---

# 🚚 Core Business APIs

---

## ➤ Get Nearest Warehouse

**GET** `/api/v1/warehouse/nearest`

### Query Parameters
- `sellerId`
- `productId`
- `quantity`

### Response
```json
{
  "warehouseId": 789,
  "warehouseLocation": {
    "lat": 12.99999,
    "long": 37.923273
  }
}
```

---

## ➤ Get Shipping Charge

**GET** `/api/v1/shipping-charge`

### Query Parameters
- `warehouseId`
- `customerId`
- `productId`
- `quantity`
- `deliverySpeed` ("standard" | "express")

### Response
```json
{
  "shippingCharge": 150.00
}
```

---

## ➤ Combined Shipping Calculation

**POST** `/api/v1/shipping-charge/calculate`

### Request
```json
{
  "sellerId": 123,
  "customerId": 456,
  "productId": 789,
  "quantity": 2,
  "deliverySpeed": "express"
}
```

### Response
```json
{
  "shippingCharge": 180.00,
  "nearestWarehouse": {
    "warehouseId": 789,
    "warehouseLocation": {
      "lat": 12.99999,
      "long": 37.923273
    }
  }
}
```

---

# 🏗️ Design Patterns Used

### Strategy Pattern
- `MiniVanStrategy`
- `TruckStrategy`
- `AirplaneStrategy`

Allows adding new transport modes without modifying core logic.

### Factory Pattern
- `transport_factory` dynamically selects strategy based on distance.

### Repository + Service Layer
- Business logic separated from route handlers.
- Clean, modular, and scalable architecture.

---

# 🧪 Testing

```bash
pytest -v
```

Covers:
- Distance calculations
- Strategy selection
- Volumetric weight logic
- Inventory validation
- API integration tests

---

# 🚀 Future Enhancements

- JWT Authentication
- Role-Based Access Control
- CI/CD Pipeline
- Kubernetes Deployment

---

# 👨‍💻 Author

Kartik Singh  
B.Tech CSE | Backend Developer
