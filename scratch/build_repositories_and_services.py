"""Generator script to build clean Python repository classes and service layers for FoodFlow."""
import json
import os
import sys

sys.path.insert(0, '.')

from data.restaurants import RESTAURANTS
from data.foods import FOODS
from data.categories import CATEGORIES
from data.cities import CITIES
from data.users import USERS
from data.orders import ORDERS
from data.offers import OFFERS
from data.reviews import REVIEWS
from data.delivery import DELIVERY_PARTNERS

os.makedirs('repositories', exist_ok=True)
os.makedirs('services', exist_ok=True)
os.makedirs('models', exist_ok=True)

# Build Repositories
rest_repo_code = f'''"""Restaurant Repository Layer providing data access and query methods."""

class RestaurantRepository:
    """Repository class for managing restaurant listings and metadata."""

    def __init__(self):
        self._restaurants = {json.dumps(RESTAURANTS, indent=4).replace('true', 'True').replace('false', 'False').replace('null', 'None')}

    def get_all(self):
        """Retrieve all active restaurant listings."""
        return [r for r in self._restaurants if r.get('is_open', True)]

    def get_by_id(self, restaurant_id):
        """Find a single restaurant by unique integer ID."""
        return next((r for r in self._restaurants if r['id'] == restaurant_id), None)

    def get_by_slug(self, slug):
        """Find a restaurant by URL slug."""
        return next((r for r in self._restaurants if r['slug'] == slug), None)

    def filter_by_cuisine(self, cuisine_name):
        """Filter restaurants matching a specific cuisine."""
        if not cuisine_name:
            return self.get_all()
        return [r for r in self.get_all() if cuisine_name in r.get('cuisines', [])]

    def filter_by_rating(self, min_rating):
        """Filter restaurants with rating >= min_rating."""
        return [r for r in self.get_all() if r.get('rating', 0.0) >= float(min_rating)]

    def filter_veg_only(self):
        """Filter pure vegetarian restaurants."""
        return [r for r in self.get_all() if r.get('is_veg_only', False)]

    def get_featured(self):
        """Retrieve featured restaurants for landing page spotlight."""
        return [r for r in self.get_all() if r.get('is_featured', False)]

    def search(self, query):
        """Perform search query against restaurant names, cuisines, and addresses."""
        if not query:
            return self.get_all()
        q = query.lower().strip()
        results = []
        for r in self.get_all():
            name_match = q in r['name'].lower()
            cuisine_match = any(q in c.lower() for c in r.get('cuisines', []))
            address_match = q in r.get('address', '').lower()
            if name_match or cuisine_match or address_match:
                results.append(r)
        return results

restaurant_repository = RestaurantRepository()
'''

with open('repositories/restaurant_repository.py', 'w', encoding='utf-8') as f:
    f.write(rest_repo_code)

food_repo_code = f'''"""Food Item Repository Layer providing catalog search, pricing, and variant access."""

class FoodRepository:
    """Repository class for managing food menu items."""

    def __init__(self):
        self._foods = {json.dumps(FOODS, indent=4).replace('true', 'True').replace('false', 'False').replace('null', 'None')}

    def get_all(self):
        """Retrieve all active food items."""
        return [f for f in self._foods if f.get('is_available', True)]

    def get_by_id(self, food_id):
        """Find a food item by unique integer ID."""
        return next((f for f in self._foods if f['id'] == food_id), None)

    def get_by_restaurant(self, restaurant_id):
        """Get all food items belonging to a specific restaurant."""
        return [f for f in self.get_all() if f['restaurant_id'] == restaurant_id]

    def get_by_category(self, category_id):
        """Get all food items belonging to a food category."""
        return [f for f in self.get_all() if f['category_id'] == category_id]

    def get_bestsellers(self):
        """Retrieve bestseller dishes across all restaurants."""
        return [f for f in self.get_all() if f.get('is_best_seller', False)]

    def filter_veg(self):
        """Retrieve vegetarian food items."""
        return [f for f in self.get_all() if f.get('is_veg', False)]

    def search(self, query):
        """Search food items by name, description, or ingredients."""
        if not query:
            return self.get_all()
        q = query.lower().strip()
        results = []
        for item in self.get_all():
            name_match = q in item['name'].lower()
            desc_match = q in item.get('description', '').lower()
            ing_match = any(q in ing.lower() for ing in item.get('ingredients', []))
            if name_match or desc_match or ing_match:
                results.append(item)
        return results

food_repository = FoodRepository()
'''

with open('repositories/food_repository.py', 'w', encoding='utf-8') as f:
    f.write(food_repo_code)

user_repo_code = f'''"""User Repository Layer for managing customer, owner, driver, and admin user data."""

class UserRepository:
    """Repository class for user account lookup and authentication."""

    def __init__(self):
        self._users = {json.dumps(USERS, indent=4).replace('true', 'True').replace('false', 'False').replace('null', 'None')}

    def get_all(self):
        """Retrieve all registered users."""
        return self._users

    def get_by_id(self, user_id):
        """Find user by unique ID."""
        return next((u for u in self._users if u['id'] == user_id), None)

    def get_by_email(self, email):
        """Find user by email address."""
        if not email:
            return None
        return next((u for u in self._users if u['email'].lower() == email.lower().strip()), None)

    def get_by_role(self, role):
        """Filter users by role (customer, restaurant, delivery, admin)."""
        return [u for u in self._users if u['role'] == role]

user_repository = UserRepository()
'''

with open('repositories/user_repository.py', 'w', encoding='utf-8') as f:
    f.write(user_repo_code)

order_repo_code = f'''"""Order Repository Layer for managing customer order records and status updates."""

class OrderRepository:
    """Repository class for order management."""

    def __init__(self):
        self._orders = {json.dumps(ORDERS, indent=4).replace('true', 'True').replace('false', 'False').replace('null', 'None')}

    def get_all(self):
        """Retrieve all order records."""
        return self._orders

    def get_by_id(self, order_id):
        """Find order by ID or order number."""
        return next((o for o in self._orders if str(o['id']) == str(order_id) or str(o.get('order_number')) == str(order_id)), None)

    def get_by_customer(self, customer_id):
        """Retrieve all orders placed by a specific customer."""
        return [o for o in self._orders if str(o.get('customer_id')) == str(customer_id)]

    def get_by_restaurant(self, restaurant_id):
        """Retrieve orders received by a specific restaurant."""
        return [o for o in self._orders if str(o.get('restaurant_id')) == str(restaurant_id)]

    def get_by_driver(self, driver_id):
        """Retrieve orders assigned to a delivery driver."""
        return [o for o in self._orders if str(o.get('delivery_agent_id')) == str(driver_id)]

order_repository = OrderRepository()
'''

with open('repositories/order_repository.py', 'w', encoding='utf-8') as f:
    f.write(order_repo_code)

print("Generated clean repositories layer!")
