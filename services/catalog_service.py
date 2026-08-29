"""Catalog Service Layer for handling business logic of restaurant & food browsing."""
from repositories.restaurant_repository import restaurant_repository
from repositories.food_repository import food_repository

class CatalogService:
    """Service class for restaurant catalog and menu browsing."""

    def get_home_restaurants(self):
        """Retrieve featured restaurants for home landing page."""
        return restaurant_repository.get_featured()

    def get_restaurant_menu(self, slug):
        """Retrieve restaurant details and grouped menu items by category."""
        restaurant = restaurant_repository.get_by_slug(slug)
        if not restaurant:
            return None, []
        
        foods = food_repository.get_by_restaurant(restaurant['id'])
        return restaurant, foods

    def filter_catalog(self, query='', cuisine='', is_veg=False, min_rating=0.0, sort_by='rating'):
        """Multi-criterion filtering for restaurant directory."""
        results = restaurant_repository.get_all()

        if query:
            results = [r for r in results if query.lower() in r['name'].lower() or any(query.lower() in c.lower() for c in r.get('cuisines', []))]

        if cuisine:
            results = [r for r in results if cuisine in r.get('cuisines', [])]

        if is_veg:
            results = [r for r in results if r.get('is_veg_only', False)]

        if min_rating > 0.0:
            results = [r for r in results if r.get('rating', 0.0) >= min_rating]

        if sort_by == 'rating':
            results.sort(key=lambda x: x.get('rating', 0.0), reverse=True)
        elif sort_by == 'delivery_time':
            results.sort(key=lambda x: x.get('delivery_time', '99'))
        elif sort_by == 'min_order':
            results.sort(key=lambda x: x.get('min_order', 0.0))

        return results

catalog_service = CatalogService()
