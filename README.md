# B2B E-Commerce Shipping Charge Estimator

A high-performance, asynchronous REST API built with FastAPI to calculate shipping charges for a B2B e-commerce marketplace. This application helps connect Kirana stores (customers) with sellers by dynamically identifying the nearest drop-off warehouses and calculating delivery costs based on distance, weight, and delivery speed.

## 🚀 Features

* **Dynamic Warehouse Routing:** Calculates the nearest warehouse for a seller using the Haversine formula.
* **Smart Shipping Calculation:** Calculates shipping costs using a Strategy Pattern based on distance (Mini Van, Truck, Aeroplane) and handles Express vs. Standard delivery.
* **Volumetric Weight Handling:** Automatically calculates both actual and volumetric weight and charges based on the higher value, simulating real-world logistics.
* **High Performance:** Fully asynchronous architecture using `FastAPI` and `SQLAlchemy (asyncpg)`.
* **Response Caching:** Integrated `Redis` caching for complex calculations to ensure blazing-fast response times.
* **Inventory Awareness:** Validates warehouse capacity and existing inventory constraints before routing sellers.

## 🛠️ Tech Stack

* **Framework:** Python 3.10+, FastAPI
* **Database:** PostgreSQL (with Asyncpg driver)
* **ORM:** SQLAlchemy (Async)
* **Caching:** Redis
* **Data Validation:** Pydantic

## 📦 Installation & Setup

### Prerequisites
* Python 3.10+
* PostgreSQL running locally or remotely
* Redis server running locally or remotely

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd shipping-estimator
```

### 2. Set up a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Update the `DATABASE_URL` in your database configuration to point to your PostgreSQL instance. Ensure Redis is running on `localhost:6379`.
```python
DATABASE_URL = "postgresql+asyncpg://<user>:<password>@<host>/<dbname>"
```

### 5. Run the Application
```bash
uvicorn app.main:app --reload
```
The application will be available at `http://localhost:8000`. You can view the interactive Swagger API documentation at `http://localhost:8000/docs`.

---

## 📖 API Documentation

### 1. Get Nearest Warehouse
Finds the closest warehouse for a seller to drop off a specific product, taking warehouse capacity into account.

* **Endpoint:** `GET /api/v1/warehouse/nearest`
* **Query Parameters:**
  * `sellerId` (int)
  * `productId` (int)
  * `quantity` (int)

**Response:**
```json
{
  "warehouseId": 789,
  "warehouseLocation": {
    "lat": 12.99999,
    "long": 37.923273
  }
}
```

### 2. Get Shipping Charge
Calculates the shipping charge from a specific warehouse to a customer based on distance and transport mode.

* **Endpoint:** `GET /api/v1/shipping-charge`
* **Query Parameters:**
  * `warehouseId` (int)
  * `customerId` (int)
  * `productId` (int)
  * `quantity` (int, default=1)
  * `deliverySpeed` (string: "standard" or "express")

**Response:**
```json
{
  "shippingCharge": 150.00
}
```

### 3. Calculate Combined Shipping
An aggregator endpoint that finds the nearest warehouse and immediately calculates the shipping charge to the customer.

* **Endpoint:** `POST /api/v1/shipping-charge/calculate`
* **Payload:**
```json
{
  "sellerId": 123,
  "customerId": 456,
  "productId": 789,
  "quantity": 2,
  "deliverySpeed": "express"
}
```

**Response:**
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

## 🏗️ Design Patterns Used
* **Strategy Pattern:** Used for calculating transportation costs (`MiniVanStrategy`, `TruckStrategy`, `AirplaneStrategy`). This allows the system to easily scale if new transportation modes (e.g., Drone Delivery, Cargo Ship) are introduced without modifying the core calculation engine.
* **Factory Pattern:** Used (`transport_factory`) to dynamically instantiate the correct transportation strategy based on distance boundaries.
* **Repository/Service Layer:** Business logic is separated from API route handlers, keeping the codebase clean and modular.