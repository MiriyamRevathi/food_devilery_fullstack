"""Content-Based & Collaborative Recommendation Engine for FoodFlow.
Generates personalized food recommendations, cross-selling combos, and trending dishes.
"""

def get_recommended_foods_for_cart(cart_items, foods_dataset):
    """
    Recommend complementary items based on items currently in cart:
    - Drinks/Beverages if missing
    - Desserts if missing
    - Popular items from same category
    """
    if not cart_items:
        # Return overall bestsellers if cart is empty
        return [f for f in foods_dataset if f.get('is_best_seller')][:6]

    cart_cat_ids = set()
    cart_food_ids = set()
    for item in cart_items:
        food_id = item.get('food_id')
        cart_food_ids.add(food_id)
        matching_food = next((f for f in foods_dataset if f['id'] == food_id), None)
        if matching_food:
            cart_cat_ids.add(matching_food['category_id'])

    recommendations = []

    # Category 7 = Desserts, Category 8 = Beverages
    has_beverage = 8 in cart_cat_ids
    has_dessert = 7 in cart_cat_ids

    # 1. Recommend Beverages if missing
    if not has_beverage:
        beverages = [f for f in foods_dataset if f['category_id'] == 8 and f['id'] not in cart_food_ids]
        recommendations.extend(beverages[:2])

    # 2. Recommend Desserts if missing
    if not has_dessert:
        desserts = [f for f in foods_dataset if f['category_id'] == 7 and f['id'] not in cart_food_ids]
        recommendations.extend(desserts[:2])

    # 3. Fill remaining with bestsellers from same restaurant
    r_id = cart_items[0].get('restaurant_id')
    same_restaurant_bestsellers = [
        f for f in foods_dataset
        if f['restaurant_id'] == r_id
        and f['id'] not in cart_food_ids
        and f not in recommendations
    ]
    recommendations.extend(same_restaurant_bestsellers[:4])

    return recommendations[:6]

def get_similar_restaurants(restaurant, restaurants_dataset):
    """Find similar restaurants based on cuisine overlap and rating tier."""
    if not restaurant:
        return []

    r_cuisines = set(restaurant.get('cuisines', []))
    similar = []

    for r in restaurants_dataset:
        if r['id'] == restaurant['id']:
            continue
        overlap = len(r_cuisines.intersection(set(r.get('cuisines', []))))
        if overlap > 0:
            similar.append((overlap, r['rating'], r))

    similar.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return [x[2] for x in similar[:6]]
