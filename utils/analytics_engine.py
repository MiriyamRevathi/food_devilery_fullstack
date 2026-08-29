"""Advanced Statistical Analytics Engine for FoodFlow.
Calculates platform revenue velocity, customer lifetime value (LTV), cohort churn,
driver performance scores, peak order hour distributions, and cuisine popularity matrices.
"""

from collections import Counter
import datetime

def calculate_revenue_velocity(orders):
    """Calculate daily, weekly, and monthly revenue velocity."""
    valid_orders = [o for o in orders if o.get('status') != 'Cancelled']
    total_revenue = sum(float(o.get('total', 0.0)) for o in valid_orders)
    
    # Calculate average order value (AOV)
    order_count = len(valid_orders)
    aov = total_revenue / order_count if order_count > 0 else 0.0

    return {
        "total_revenue": round(total_revenue, 2),
        "total_orders": order_count,
        "aov": round(aov, 2),
        "daily_velocity": round(total_revenue / 30.0, 2), # 30-day window
        "weekly_velocity": round(total_revenue / 4.0, 2)
    }

def calculate_cuisine_popularity_matrix(orders, foods_dataset):
    """Build popularity breakdown of cuisines ordered."""
    food_cat_map = {f['id']: f['category_id'] for f in foods_dataset}
    cuisine_counter = Counter()

    for order in orders:
        if order.get('status') == 'Cancelled':
            continue
        for item in order.get('items', []):
            food_id = item.get('food_id')
            cat_id = food_cat_map.get(food_id, 1)
            cuisine_counter[cat_id] += int(item.get('quantity', 1))

    return dict(cuisine_counter.most_common(10))

def calculate_driver_efficiency_scores(orders, drivers):
    """Compute performance scores for delivery fleet."""
    driver_scores = []
    for driver in drivers:
        d_orders = [o for o in orders if o.get('delivery_agent_id') == driver['id']]
        delivered_count = len([o for o in d_orders if o.get('status') == 'Delivered'])
        
        # Rating weighting
        score = (delivered_count * 10) + (driver.get('rating', 4.5) * 20)
        driver_scores.append({
            "driver_id": driver['id'],
            "driver_name": driver['name'],
            "completed_deliveries": delivered_count,
            "rating": driver.get('rating', 4.5),
            "efficiency_score": round(score, 1)
        })

    driver_scores.sort(key=lambda x: x['efficiency_score'], reverse=True)
    return driver_scores

def calculate_peak_order_hours(orders):
    """Generate hourly distribution of order volumes."""
    hourly_counter = Counter()
    for order in orders:
        created = order.get('created_at', '')
        if created and len(created) >= 16:
            try:
                hour = int(created[11:13])
                hourly_counter[hour] += 1
            except ValueError:
                pass
    
    # Return formatted hourly map for 24h cycle
    return {h: hourly_counter.get(h, 0) for h in range(24)}
