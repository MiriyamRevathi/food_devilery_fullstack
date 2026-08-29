from catalog.food_catalog_part_01 import FOOD_CATALOG_PART_01
from catalog.food_catalog_part_02 import FOOD_CATALOG_PART_02
from catalog.food_catalog_part_03 import FOOD_CATALOG_PART_03
from catalog.food_catalog_part_04 import FOOD_CATALOG_PART_04
from catalog.food_catalog_part_05 import FOOD_CATALOG_PART_05
from catalog.food_catalog_part_06 import FOOD_CATALOG_PART_06
from catalog.food_catalog_part_07 import FOOD_CATALOG_PART_07


class FoodRepository:
    """Repository for the complete FoodFlow food catalog."""

    def __init__(self):
        self._foods = [food for part in (FOOD_CATALOG_PART_01, FOOD_CATALOG_PART_02, FOOD_CATALOG_PART_03, FOOD_CATALOG_PART_04, FOOD_CATALOG_PART_05, FOOD_CATALOG_PART_06, FOOD_CATALOG_PART_07,) for food in part]

    def get_all(self):
        """Retrieve all active food items."""
        return [food for food in self._foods if food.get("is_available", True)]

    def get_by_id(self, food_id):
        """Find a food item by unique integer ID."""
        return next((food for food in self._foods if food["id"] == food_id), None)

    def get_by_restaurant(self, restaurant_id):
        """Get all food items belonging to a restaurant."""
        return [food for food in self.get_all() if food["restaurant_id"] == restaurant_id]

    def get_by_category(self, category_id):
        """Get all food items belonging to a category."""
        return [food for food in self.get_all() if food["category_id"] == category_id]

    def get_bestsellers(self):
        """Retrieve bestseller dishes across all restaurants."""
        return [food for food in self.get_all() if food.get("is_best_seller", False)]

    def filter_veg(self):
        """Retrieve vegetarian food items."""
        return [food for food in self.get_all() if food.get("is_veg", False)]

    def search(self, query):
        """Search food names, descriptions, and ingredients."""
        if not query:
            return self.get_all()
        normalized = query.lower().strip()
        return [
            food for food in self.get_all()
            if normalized in food["name"].lower()
            or normalized in food.get("description", "").lower()
            or any(normalized in ingredient.lower() for ingredient in food.get("ingredients", []))
        ]


food_repository = FoodRepository()
