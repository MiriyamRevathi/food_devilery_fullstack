# FoodFlow

FoodFlow is a runnable Flask food-delivery web application. It supports the customer ordering journey alongside restaurant, delivery-partner, and administrator portals. The project uses local in-memory datasets, so it can start without a database or third-party API.

## What is included

- Customer restaurant search, menus, cart, promo codes, checkout, order tracking, favourites, and addresses.
- Restaurant menu and order management.
- Delivery status workflow and earnings tracking.
- Administration for users, restaurants, promotions, cities, diagnostics, and reports.
- Modular Flask blueprints, templates, CSS/JavaScript, service and repository layers, plus automated tests.

## Requirements and dependency files

Use Python 3.10 or newer. The project provides standard dependency metadata for both pip and Pipenv.

| File | Purpose |
| --- | --- |
| `requirements.txt` | Pinned pip dependency manifest |
| `requirements.lock` | Hash-pinned pip installation lockfile |
| `pyproject.toml` | Standard Python project metadata and pytest configuration |
| `Pipfile` / `Pipfile.lock` | Pipenv manifest and recognized lockfile |

## Run locally

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` in a browser.

For a hash-verified installation:

```bash
pip install --require-hashes -r requirements.lock
```

For Pipenv:

```bash
pipenv sync --dev
pipenv run python app.py
```

## Run with Docker

```bash
docker build -t foodflow .
docker run --rm -p 5000:5000 foodflow
```

## Test

```bash
pytest
```

## Demo accounts

| Role | Email | Password |
| --- | --- | --- |
| Customer | `customer@foodflow.local` | `customer123` |
| Restaurant partner | `restaurant@foodflow.local` | `restaurant123` |
| Delivery partner | `delivery@foodflow.local` | `delivery123` |
| Administrator | `admin@foodflow.local` | `admin123` |

## Project layout

`app.py` creates the Flask application and registers route blueprints in `routes/`. Domain data is in `data/`; business logic and data access live in `services/` and `repositories/`. The 1,040-item repository catalog is partitioned into importable modules in `catalog/`, avoiding a single oversized source file while keeping `FoodRepository`'s interface stable. Views and browser assets are under `templates/` and `static/`. `tests/` contains automated tests, and `wsgi.py` exposes the app to production WSGI servers.
