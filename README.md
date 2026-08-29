# 🚴‍♂️ FoodFlow — Master Food Delivery Web Application

**FoodFlow** is a large, feature-rich, polished food-delivery platform built with **Python 3.10**, **Flask**, **HTML5**, **CSS3**, and **Vanilla JavaScript**. It provides complete end-to-end functionality for Customers, Restaurant Owners, Delivery Partners, and System Administrators without requiring external database engines, JWT, or cloud APIs.

---

## 🌟 Key Features & Role Portals

### 👤 1. Customer Experience
- **Home Landing Page**: Hero banner with quick search, popular category grid, active promo coupons carousel, featured restaurants, trending dishes, and platform advantage cards.
- **Restaurant Directory & Multi-Filter**: Search by name/cuisine, filter by cuisine type, pure veg indicator (`veg=1`), rating threshold (`★ 4.0+`, `★ 4.5+`), and sort by rating, fastest delivery time, or popularity.
- **Restaurant Menu Page**: Hero cover banner, rating stats, address, opening hours, sticky menu category nav tabs, dish listings, and customer reviews.
- **Food Customization Modal**: Select portion sizes/variants (e.g. Single Portion, Family Pack) and add-on toppings with real-time price calculation.
- **Interactive Shopping Cart**: Quantity adjustments (+/-), single-restaurant order validation, coupon engine (`WELCOME50`, `FOOD20`, `SAVE100`), subtotal, discount, delivery fee, 5% GST tax calculation.
- **Multi-Step Checkout & Simulated Payment**: Pre-filled delivery address, phone, special cooking notes, and 3 payment simulation options:
  - 💵 **Cash on Delivery (COD)**
  - 💳 **Demo Credit / Debit Card Payment**
  - 📱 **Demo Instant UPI Payment (GooglePay / PhonePe / Paytm)**
- **Order System & Live Tracking**:
  - Customer order history page with status pills (`Order Placed`, `Preparing`, `Out for Delivery`, `Delivered`, `Cancelled`).
  - Detailed order view with status history audit log.
  - Simulated live order tracking view with animated progress stepper (`✓ Placed` → `✓ Confirmed` → `✓ Preparing` → `○ Ready` → `○ Out for Delivery` → `○ Delivered`).
  - Delivery agent profile spotlight card (Ramesh Kumar, Honda Activa) with one-click call simulation.
  - Interactive map grid simulator displaying restaurant, courier en-route, and destination pins.
  - Reorder, saved addresses (`/addresses`), wishlist favorites (`/favorites`), and cancellation features.

### 🍳 2. Restaurant Owner Portal (`/restaurant/dashboard`)
- **Overview Metrics**: Total Revenue, Total Orders, Today's Orders, Pending Orders counter, Average Rating.
- **Kitchen Order Fulfillment Center**: Real-time status update dropdowns (`Order Placed`, `Confirmed`, `Preparing`, `Ready for Pickup`, `Out for Delivery`, `Delivered`).
- **Menu Management Catalog**: Add new dishes, edit pricing, toggle availability (In Stock / Out of Stock), change discounts.
- **Inventory Tracker**: Kitchen raw materials, ingredients stock monitoring (`/restaurant/inventory`).
- **Customer Reviews & Ratings**: View reviews submitted by customers.
- **Analytics Reports**: Revenue summary, average order value (AOV), and pure CSS weekly sales performance bar chart.

### 🛵 3. Delivery Partner Portal (`/delivery/dashboard`)
- **Overview Dashboard**: Today's Earnings, Total Lifetime Earnings, Completed Deliveries counter, Driver Rating, active order spotlight card.
- **Active Delivery Stepper**: Step-by-step progress update controls:
  - `Confirmed` → `Preparing` → `Ready for Pickup` → `Out for Delivery` → `Delivered` (+₹50.00 Payout reward).
- **Earnings Breakdown & Payout Log**: View completed delivery payouts and lifetime earnings.

### ⚡ 4. Administrator Control Panel (`/admin/dashboard`)
- **System Overview**: Gross Platform Revenue, Total Orders, Registered Users, Restaurant Partners counter.
- **User Accounts Audit**: Manage Customer, Restaurant Partner, Delivery Agent, and Admin accounts.
- **Restaurant Listings Audit**: Toggle Open/Closed status and Featured status.
- **Global Orders Control Center**: Master order monitoring and manual status overrides.
- **Promo Coupon Control**: Create new promo codes (set discount types, minimum spend, expiration).
- **Multi-City Delivery Hubs**: Manage operational delivery cities and postal hubs (`/admin/cities`).
- **System Health Diagnostics**: Server performance monitoring and cache health (`/admin/diagnostics`).
- **Analytics Reports**: Pure JS/CSS order status distribution progress bars and platform metrics.

---

## 🛠️ Technology Stack & Dependency Documentation

- **Backend**: Python 3.10+, Flask 3.0+, Werkzeug, Flask Sessions
- **Frontend**: HTML5, CSS3 (CSS Variables, Flexbox, Grid), Vanilla JavaScript (Zero jQuery / React / Node)
- **Testing**: Pytest 8.0+
- **Dependency Manifest**: `requirements.txt`
- **Lockfile**: `requirements.lock` (Deterministic hash-pinned dependency lockfile)

---

## 🔑 Pre-Configured Demo Accounts

You can test any role instantly using the **One-Click Demo Login** buttons on the `/login` page or use the credentials below:

| Role | Email | Password | Dashboard Link |
| :--- | :--- | :--- | :--- |
| **Customer** | `customer@foodflow.local` | `customer123` | `/` |
| **Restaurant Partner** | `restaurant@foodflow.local` | `restaurant123` | `/restaurant/dashboard` |
| **Delivery Agent** | `delivery@foodflow.local` | `delivery123` | `/delivery/dashboard` |
| **Administrator** | `admin@foodflow.local` | `admin123` | `/admin/dashboard` |

---

## 📂 Directory Structure

```text
food delivery onr/
├── app.py                      # Flask Application entrypoint & blueprint registration
├── config.py                   # App configuration & session parameters
├── requirements.txt            # Python dependencies manifest
├── requirements.lock           # Hash-pinned dependency lockfile
├── pytest.ini                  # Pytest configuration
├── README.md                   # Project documentation
│
├── repositories/               # Repository Data Access Layer
│   ├── restaurant_repository.py# Restaurant listings & query repository
│   ├── food_repository.py      # Food menu catalog & variant repository
│   ├── user_repository.py      # User account repository
│   └── order_repository.py     # Order history repository
│
├── services/                   # Business Logic & Service Layer
│   ├── catalog_service.py      # Restaurant & menu catalog service
│   ├── cart_service.py         # Cart management & coupon service
│   └── order_service.py        # Order fulfillment & tracking service
│
├── data/                       # Domain Datasets
│   ├── categories.py           # Food categories
│   ├── restaurants.py          # 104 Detailed restaurants
│   ├── foods.py                # 1,040 Food items with macros & allergens
│   ├── cities.py               # 8 Major Indian cities & delivery zones
│   ├── users.py                # User accounts dataset
│   ├── orders.py               # Order records
│   ├── reviews.py              # Customer reviews dataset
│   ├── offers.py               # Active promo coupons
│   └── delivery.py             # Delivery partner fleet dataset
│
├── routes/                     # Modular Blueprints
│   ├── main.py                 # Landing page, search, static pages
│   ├── auth.py                 # Login, register, logout, profile
│   ├── customer.py             # Browsing, menu, cart, checkout, tracking, favorites
│   ├── restaurant.py          # Restaurant dashboard, menu CRUD, order fulfillment, inventory
│   ├── delivery.py             # Delivery dashboard, active stepper, earnings
│   ├── admin.py                # Admin panel, user audit, multi-city, diagnostics
│   └── api.py                  # Local REST API endpoints
│
├── utils/                      # Helper & Business Logic Modules
│   ├── analytics_engine.py     # Revenue velocity & driver efficiency scores
│   ├── recommendation_engine.py# Content-based recommendation algorithm
│   ├── geo_helpers.py          # Haversine distance & ETA calculator
│   ├── pdf_generator.py        # Printable tax invoice generator
│   ├── export_helpers.py       # CSV order report exporter
│   ├── notification_engine.py  # Notification queue
│   ├── calculations.py         # Subtotal, tax, & delivery fee calculations
│   └── decorators.py           # @login_required & @role_required protection
│
├── templates/                  # Jinja2 HTML Templates
├── static/                     # CSS stylesheets & Vanilla JS modules
└── tests/                      # Automated Pytest Test Suite
```

---

## ⚡ Installation & Build Instructions

### 1. Standard Installation (from Manifest)
```bash
pip install -r requirements.txt
```

### 2. Lockfile Deterministic Installation (from Lockfile)
```bash
pip install --require-hashes -r requirements.lock
```

### 3. Run Flask Web Server
```bash
python app.py
```

### 4. Open in Browser
Open `http://127.0.0.1:5000` in your web browser.

---

## 🧪 Running Automated Tests

Run the Pytest suite to execute unit and integration tests:
```bash
pytest
```
Expected output:
```text
tests/test_analytics.py ....                                             [ 17%]
tests/test_api.py ....                                                   [ 34%]
tests/test_app.py ........                                               [ 69%]
tests/test_export.py ..                                                  [ 78%]
tests/test_geo.py ..                                                     [ 86%]
tests/test_notifications.py .                                            [ 91%]
tests/test_recommendations.py ..                                         [100%]
============================= 23 passed in 0.82s ==============================
```
