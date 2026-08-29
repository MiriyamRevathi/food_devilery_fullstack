"""Geographic ETA, Distance (Haversine formula), and Delivery Fee Matrix Calculator."""
import math

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees).
    Returns distance in kilometers.
    """
    R = 6371.0 # Radius of earth in kilometers

    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dLon / 2) * math.sin(dLon / 2))
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return round(distance, 2)

def estimate_delivery_eta_and_fee(restaurant_lat, restaurant_lng, customer_lat, customer_lng):
    """
    Estimate delivery travel time (minutes) and distance-based delivery fee.
    """
    distance_km = calculate_haversine_distance(restaurant_lat, restaurant_lng, customer_lat, customer_lng)
    
    # Base prep time 15 mins + 3 mins per km
    estimated_mins = int(15 + (distance_km * 3.5))
    
    # Fee matrix: ₹30 base + ₹10 per km over 3 km
    if distance_km <= 3.0:
        delivery_fee = 30.0
    else:
        delivery_fee = 30.0 + ((distance_km - 3.0) * 10.0)

    return {
        "distance_km": distance_km,
        "estimated_mins": estimated_mins,
        "eta_range": f"{estimated_mins - 5}-{estimated_mins + 5} min",
        "delivery_fee": round(delivery_fee, 2)
    }
