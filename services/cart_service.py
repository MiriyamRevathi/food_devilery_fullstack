"""Cart Service Layer for handling cart validations, calculations, and promo codes."""
from utils.calculations import calculate_cart_totals
from repositories.food_repository import food_repository

class CartService:
    """Service class for managing shopping cart operations."""

    def add_item_to_cart(self, current_cart, food_id, quantity=1, variant=None, add_ons=None):
        """Add or update an item in the cart session."""
        food = food_repository.get_by_id(food_id)
        if not food:
            return False, "Food item not found", current_cart

        # Check if cart contains items from a different restaurant
        if current_cart:
            first_r_id = current_cart[0].get('restaurant_id')
            if first_r_id and first_r_id != food['restaurant_id']:
                return False, "Cart contains items from a different restaurant. Clear cart to proceed?", current_cart

        # Calculate item price with variant & add-ons
        unit_price = float(food.get('discount_price', food['price']))
        variant_price = 0.0
        if variant and food.get('variants'):
            match_v = next((v for v in food['variants'] if v['name'] == variant), None)
            if match_v:
                variant_price = float(match_v.get('price', 0.0))

        addon_price = 0.0
        if add_ons and food.get('add_ons'):
            for addon_name in add_ons:
                match_a = next((a for a in food['add_ons'] if a['name'] == addon_name), None)
                if match_a:
                    addon_price += float(match_a.get('price', 0.0))

        item_total = (unit_price + variant_price + addon_price) * quantity

        # Update existing item if matching food_id & variant
        existing = next((item for item in current_cart if item['food_id'] == food_id and item.get('variant') == variant), None)
        if existing:
            existing['quantity'] += quantity
            existing['price'] = unit_price + variant_price + addon_price
        else:
            current_cart.append({
                'food_id': food['id'],
                'restaurant_id': food['restaurant_id'],
                'name': food['name'],
                'price': unit_price + variant_price + addon_price,
                'quantity': quantity,
                'variant': variant or 'Regular',
                'add_ons': add_ons or []
            })

        return True, "Item added to cart", current_cart

    def compute_totals(self, cart_items, coupon_code=None):
        """Compute financial totals for cart."""
        return calculate_cart_totals(cart_items, coupon_code=coupon_code)

cart_service = CartService()
