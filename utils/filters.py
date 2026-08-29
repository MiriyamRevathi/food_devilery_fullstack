"""Multi-criterion search, filtering, and sorting algorithms."""
from data.restaurants import RESTAURANTS
from data.foods import FOODS
from data.categories import CATEGORIES

def filter_restaurants(query=None, cuisine=None, is_veg=False, min_rating=0.0, sort_by=None):
    """
    Filter and sort restaurant collection:
    - Search by name, cuisine, address
    - Cuisine filter
    - Veg-only filter
    - Rating threshold
    - Sorting by rating, delivery_time, popularity, price
    """
    results = list(RESTAURANTS)
    
    if query:
        q = query.lower().strip()
        results = [
            r for r in results
            if q in r["name"].lower()
            or any(q in c.lower() for c in r["cuisines"])
            or q in r["address"].lower()
            or q in r.get("description", "").lower()
        ]
        
    if cuisine:
        c_filter = cuisine.lower().strip()
        results = [
            r for r in results
            if any(c.lower() == c_filter for c in r["cuisines"])
        ]
        
    if is_veg:
        results = [r for r in results if r["is_veg_only"]]
        
    if min_rating > 0:
        results = [r for r in results if r["rating"] >= min_rating]
        
    if sort_by == "rating":
        results.sort(key=lambda r: r["rating"], reverse=True)
    elif sort_by == "delivery_time":
        # Extract lower bound of delivery time string e.g. "20-25 min" -> 20
        def get_min_time(r):
            try:
                return int(r["delivery_time"].split("-")[0].strip())
            except Exception:
                return 999
        results.sort(key=get_min_time)
    elif sort_by == "popularity":
        results.sort(key=lambda r: r["review_count"], reverse=True)
        
    return results

def search_food_items(query):
    """Search food items across names, descriptions, and category names."""
    if not query:
        return []
    q = query.lower().strip()
    matches = []
    
    # Map category ID to name
    cat_map = {c["id"]: c["name"].lower() for c in CATEGORIES}
    
    for food in FOODS:
        cat_name = cat_map.get(food["category_id"], "")
        if (q in food["name"].lower() or 
            q in food["description"].lower() or 
            q in cat_name):
            matches.append(food)
            
    return matches
