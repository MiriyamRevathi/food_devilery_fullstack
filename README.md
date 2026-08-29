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
- **Dependency Manifest**: `requirements.txt`, `Pipfile`, `pyproject.toml`
- **Lockfile**: `requirements.lock`, `Pipfile.lock` (Deterministic hash-pinned dependency lockfile)

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
