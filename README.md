# FoodFlow — Food Delivery Web Application

FoodFlow is a full-stack food delivery web application built with **Python, Flask, HTML, CSS, and Vanilla JavaScript**.

The project provides separate interfaces for customers, restaurant owners, delivery partners, and administrators. It is designed to run locally without an external database, cloud API, or payment gateway. Application data is stored using local Python data structures and files.

## Features

### Customer

Customers can:

* Browse and search restaurants
* Filter restaurants by cuisine, rating, and vegetarian options
* View restaurant menus and food details
* Customize food items with variants and add-ons
* Add and manage items in the shopping cart
* Apply promotional coupons
* Enter delivery details during checkout
* Simulate COD, card, and UPI payments
* View previous orders
* Track orders through different delivery stages
* Reorder previous purchases
* Save delivery addresses
* Manage favourite restaurants and dishes
* Cancel eligible orders
* View delivery partner information

### Restaurant Owner

The restaurant dashboard includes:

* Revenue and order statistics
* Pending order management
* Order status updates
* Menu management
* Food availability controls
* Pricing and discount management
* Inventory tracking
* Customer reviews
* Sales and revenue analytics

### Delivery Partner

Delivery partners can:

* View active deliveries
* Update delivery status
* Track completed deliveries
* View daily earnings
* View lifetime earnings
* View delivery payout history
* Monitor driver rating

### Administrator

The admin dashboard provides:

* Platform-wide revenue and order statistics
* User account management
* Restaurant management
* Order monitoring and status controls
* Promotional coupon management
* City and delivery hub management
* System diagnostics
* Platform analytics

## Technology Stack

| Component      | Technology                      |
| -------------- | ------------------------------- |
| Backend        | Python 3.10+, Flask             |
| Frontend       | HTML5, CSS3, Vanilla JavaScript |
| Templates      | Jinja2                          |
| Testing        | Pytest                          |
| Data Storage   | Local Python data / files       |
| Authentication | Flask Sessions                  |
| Deployment     | Docker                          |

No React, Node.js, external database, cloud API, or real payment gateway is required.

## Demo Accounts

The application includes demo accounts for testing the different user roles.

| Role       | Email                       | Password        |
| ---------- | --------------------------- | --------------- |
| Customer   | `customer@foodflow.local`   | `customer123`   |
| Restaurant | `restaurant@foodflow.local` | `restaurant123` |
| Delivery   | `delivery@foodflow.local`   | `delivery123`   |
| Admin      | `admin@foodflow.local`      | `admin123`      |

You can also use the demo-login options available on the login page.

## Project Structure

```text
foodflow/
├── app.py
├── config.py
├── requirements.txt
├── requirements.lock
├── pytest.ini
├── README.md
│
├── repositories/
│   ├── restaurant_repository.py
│   ├── food_repository.py
│   ├── user_repository.py
│   └── order_repository.py
│
├── services/
│   ├── catalog_service.py
│   ├── cart_service.py
│   └── order_service.py
│
├── data/
│   ├── categories.py
│   ├── restaurants.py
│   ├── foods.py
│   ├── cities.py
│   ├── users.py
│   ├── orders.py
│   ├── reviews.py
│   ├── offers.py
│   └── delivery.py
│
├── routes/
│   ├── main.py
│   ├── auth.py
│   ├── customer.py
│   ├── restaurant.py
│   ├── delivery.py
│   ├── admin.py
│   └── api.py
│
├── utils/
│   ├── analytics_engine.py
│   ├── recommendation_engine.py
│   ├── geo_helpers.py
│   ├── pdf_generator.py
│   ├── export_helpers.py
│   ├── notification_engine.py
│   ├── calculations.py
│   └── decorators.py
│
├── templates/
├── static/
└── tests/
```

## Installation

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

For a hash-verified installation:

```bash
pip install --require-hashes -r requirements.lock
```

### 2. Start the application

```bash
python app.py
```

### 3. Open the website

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

## Testing

Run the complete test suite with:

```bash
pytest
```

The project includes tests covering application routes, analytics, APIs, recommendations, notifications, exports, and geographic calculations.

## Docker

Build the Docker image:

```bash
docker build -t foodflow:latest .
```

Run the application:

```bash
docker run -p 5000:5000 foodflow:latest
```

Then visit:

```text
http://127.0.0.1:5000
```

## Application Flow

The main customer workflow is:

```text
Browse Restaurants
       ↓
View Menu
       ↓
Customize Food
       ↓
Add to Cart
       ↓
Apply Coupon
       ↓
Checkout
       ↓
Payment Simulation
       ↓
Order Placed
       ↓
Restaurant Preparation
       ↓
Delivery
       ↓
Order Delivered
```

Restaurant, delivery, and administrator portals provide the corresponding management workflows around the same order lifecycle.

## Local-First Design

FoodFlow is intended primarily as a local demonstration and development project.

* No external database is required.
* No cloud services are required.
* Payment processing is simulated.
* Restaurant and user data are local.
* Order processing runs inside the Flask application.
* Models such as recommendations and delivery calculations run locally.
* Uploaded or generated application data remains within the project environment.

## Project Purpose

The goal of FoodFlow is to demonstrate how a complete food-delivery platform can be structured using a lightweight Python/Flask backend and a traditional HTML, CSS, and JavaScript frontend.

It focuses on application architecture, role-based workflows, business logic, order management, and a realistic user experience while keeping the setup simple enough to run on a local machine.
