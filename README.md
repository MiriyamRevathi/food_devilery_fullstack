# 🚴‍♂️ FoodFlow — Master Food Delivery Web Application

**FoodFlow** is a large, feature-rich, polished food-delivery platform built with **Python 3.10**, **Flask**, **HTML5**, **CSS3**, and **Vanilla JavaScript**. It provides complete end-to-end functionality for Customers, Restaurant Owners, Delivery Partners, and System Administrators without requiring a database engine, JWT, or external cloud APIs.

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
  - Reorder & order cancellation features.

### 🍳 2. Restaurant Owner Portal (`/restaurant/dashboard`)
- **Overview Metrics**: Total Revenue, Total Orders, Today's Orders, Pending Orders counter, Average Rating.
- **Kitchen Order Fulfillment Center**: Real-time status update dropdowns (`Order Placed`, `Confirmed`, `Preparing`, `Ready for Pickup`, `Out for Delivery`, `Delivered`).
- **Menu Management Catalog**: Add new dishes, edit pricing, toggle availability (In Stock / Out of Stock), change discounts.
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
- **Analytics Reports**: Pure JS/CSS order status distribution progress bars and platform metrics.

### 🌙 5. Global Frontend Features
- **Dark Mode**: Instant light/dark theme switcher with `localStorage` persistence.
- **Toast Notifications**: Dynamic toast notification system for instant feedback.
- **Responsive Layout**: Mobile-first drawer navigation and responsive grid breakpoints (`< 576px`, `< 768px`, `< 992px`, `< 1200px`).

---

## 🛠️ Technology Stack

- **Backend**: Python 3.10+, Flask 3.0+, Werkzeug, Flask Sessions
- **Frontend**: HTML5, CSS3 (CSS Variables, Flexbox, Grid), Vanilla JavaScript (Zero jQuery / React / Node)
- **Testing**: Pytest 8.0+

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

## 📁 Directory Structure

```text
food delivery onr/
├── app.py                      # Flask Application entrypoint & blueprint registration
├── config.py                   # App configuration & session parameters
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── README.md                   # Project documentation
│
├── data/                       # Local In-Memory Data Store
│   ├── categories.py           # 12 Food categories
│   ├── restaurants.py          # 20+ Seed restaurants
│   ├── foods.py                # 100+ Seed food items
│   ├── users.py                # Hashed password demo accounts
│   ├── orders.py               # Seed orders & order state manager
│   ├── reviews.py              # Customer reviews dataset
│   ├── offers.py               # Active promo coupons (WELCOME50, FOOD20, SAVE100)
│   └── delivery.py             # Delivery partner fleet dataset
│
├── routes/                     # Modular Blueprints
│   ├── main.py                 # Landing page, search, static pages
│   ├── auth.py                 # Login, register, logout, profile
│   ├── customer.py             # Browsing, menu, cart, checkout, tracking
│   ├── restaurant.py          # Restaurant dashboard, menu CRUD, order fulfillment
│   ├── delivery.py             # Delivery dashboard, active stepper, earnings
│   └── admin.py                # Master admin panel, user audit, reports
│
├── utils/                      # Helper & Business Logic Modules
│   ├── helpers.py              # Currency (₹), star generator, time ago formatters
│   ├── validators.py           # Email, phone, password validators
│   ├── calculations.py         # Subtotal, discount, delivery fee, tax calculations
│   ├── filters.py              # Search & multi-criterion filter algorithms
│   └── decorators.py           # @login_required & @role_required protection
│
├── templates/                  # Jinja2 HTML Templates
│   ├── base.html               # Global wrapper layout
│   ├── components/             # Reusable UI macros (Navbar, Footer, Modal)
│   ├── customer/               # Customer template views
│   ├── auth/                   # Login & Register views
│   ├── restaurant/             # Restaurant dashboard views
│   ├── delivery/               # Delivery dashboard views
│   ├── admin/                  # Admin control panel views
│   └── errors/                 # 404, 403, 500 pages
│
├── static/                     # Assets
│   ├── css/                    # Modular CSS stylesheets (style, navbar, footer, home, restaurant, food, cart, checkout, orders, dashboard, admin, delivery, responsive, dark-mode)
│   └── js/                     # Vanilla JavaScript modules (main, navigation, dark-mode, search, filters, cart, validation, charts)
│
└── tests/                      # Automated Test Suite
    └── test_app.py             # Pytest automated test cases
```

---

## ⚡ Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Flask Web Server
```bash
python app.py
```

### 3. Open in Browser
Open `http://127.0.0.1:5000` in your web browser.

---

## 🧪 Running Automated Tests

Run the Pytest suite to execute unit and integration tests:
```bash
pytest
```
Expected output:
```text
tests/test_app.py ........                                               [100%]
============================== 8 passed in 0.81s ==============================
```
