"""Restaurant Partner Blueprint for managing menu, fulfilling orders, and analytics."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from data.restaurants import RESTAURANTS
from data.foods import FOODS
from data.categories import CATEGORIES
from data.orders import ORDERS, get_all_orders, get_order_by_id, update_order_status
from data.reviews import REVIEWS
from utils.decorators import role_required

restaurant_bp = Blueprint('restaurant', __name__, url_prefix='/restaurant')

def get_current_restaurant():
    """Helper to get restaurant associated with logged in restaurant owner."""
    user = session.get('user', {})
    r_id = user.get('restaurant_id', 1) # Default to restaurant ID 1 if unspecified
    return next((r for r in RESTAURANTS if r['id'] == r_id), RESTAURANTS[0])

@restaurant_bp.route('/dashboard')
@role_required('restaurant', 'admin')
def dashboard():
    """Restaurant partner overview dashboard with metrics and recent orders."""
    current_r = get_current_restaurant()
    r_id = current_r['id']

    # Filter data for this restaurant
    r_orders = [o for o in get_all_orders() if o['restaurant_id'] == r_id]
    r_foods = [f for f in FOODS if f['restaurant_id'] == r_id]
    r_reviews = [r for r in REVIEWS if r['restaurant_id'] == r_id]

    total_revenue = sum(o['total'] for o in r_orders if o['status'] != 'Cancelled')
    today_orders = len(r_orders)
    pending_orders = len([o for o in r_orders if o['status'] in ['Order Placed', 'Confirmed', 'Preparing']])

    metrics = {
        "total_revenue": total_revenue,
        "total_orders": len(r_orders),
        "today_orders": today_orders,
        "pending_orders": pending_orders,
        "total_dishes": len(r_foods),
        "average_rating": current_r['rating']
    }

    return render_template(
        'restaurant/dashboard.html',
        restaurant=current_r,
        metrics=metrics,
        recent_orders=r_orders[:5],
        foods=r_foods[:5]
    )

@restaurant_bp.route('/orders', methods=['GET', 'POST'])
@role_required('restaurant', 'admin')
def manage_orders():
    """Restaurant order fulfillment portal with status updates."""
    current_r = get_current_restaurant()
    r_id = current_r['id']

    if request.method == 'POST':
        order_id = request.form.get('order_id')
        new_status = request.form.get('status')
        if order_id and new_status:
            update_order_status(order_id, new_status)
            flash(f"Order status updated to '{new_status}'.", "success")
            return redirect(url_for('restaurant.manage_orders'))

    r_orders = [o for o in get_all_orders() if o['restaurant_id'] == r_id]
    return render_template('restaurant/orders.html', restaurant=current_r, orders=r_orders)

@restaurant_bp.route('/menu')
@role_required('restaurant', 'admin')
def menu():
    """Menu management view displaying all food items."""
    current_r = get_current_restaurant()
    r_foods = [f for f in FOODS if f['restaurant_id'] == current_r['id']]
    return render_template('restaurant/menu.html', restaurant=current_r, foods=r_foods)

@restaurant_bp.route('/food/add', methods=['GET', 'POST'])
@role_required('restaurant', 'admin')
def add_food():
    """Add a new dish to restaurant menu."""
    current_r = get_current_restaurant()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category_id = int(request.form.get('category_id', 1))
        description = request.form.get('description', '').strip()
        price = float(request.form.get('price', 0.0))
        discount_price = float(request.form.get('discount_price', price))
        is_veg = request.form.get('is_veg') == '1'
        image = request.form.get('image', '').strip() or "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&auto=format&fit=crop&q=80"

        if name and price > 0:
            new_id = max(f['id'] for f in FOODS) + 1
            new_dish = {
                "id": new_id,
                "restaurant_id": current_r['id'],
                "category_id": category_id,
                "name": name,
                "description": description,
                "price": price,
                "discount_price": discount_price,
                "rating": 5.0,
                "is_veg": is_veg,
                "is_best_seller": False,
                "is_available": True,
                "image": image,
                "variants": [],
                "add_ons": []
            }
            FOODS.append(new_dish)
            flash(f"New dish '{name}' added to your menu!", "success")
            return redirect(url_for('restaurant.menu'))

        flash("Please provide valid dish name and price.", "danger")

    return render_template('restaurant/add_food.html', restaurant=current_r, categories=CATEGORIES)

@restaurant_bp.route('/food/toggle/<int:food_id>', methods=['POST'])
@role_required('restaurant', 'admin')
def toggle_food(food_id):
    """Toggle availability of dish (In Stock / Out of Stock)."""
    food = next((f for f in FOODS if f['id'] == food_id), None)
    if food:
        food['is_available'] = not food.get('is_available', True)
        status_text = "In Stock" if food['is_available'] else "Out of Stock"
        flash(f"'{food['name']}' status set to {status_text}.", "info")
    return redirect(url_for('restaurant.menu'))

@restaurant_bp.route('/food/edit/<int:food_id>', methods=['GET', 'POST'])
@role_required('restaurant', 'admin')
def edit_food(food_id):
    """Edit dish details."""
    food = next((f for f in FOODS if f['id'] == food_id), None)
    if not food:
        abort(404)

    current_r = get_current_restaurant()

    if request.method == 'POST':
        food['name'] = request.form.get('name', food['name']).strip()
        food['description'] = request.form.get('description', food['description']).strip()
        food['price'] = float(request.form.get('price', food['price']))
        food['discount_price'] = float(request.form.get('discount_price', food['discount_price']))
        food['is_veg'] = request.form.get('is_veg') == '1'
        if request.form.get('image'):
            food['image'] = request.form.get('image').strip()

        flash(f"Dish '{food['name']}' updated successfully!", "success")
        return redirect(url_for('restaurant.menu'))

    return render_template('restaurant/edit_food.html', restaurant=current_r, food=food, categories=CATEGORIES)

@restaurant_bp.route('/reviews')
@role_required('restaurant', 'admin')
def reviews():
    """Restaurant reviews overview."""
    current_r = get_current_restaurant()
    r_reviews = [r for r in REVIEWS if r['restaurant_id'] == current_r['id']]
    return render_template('restaurant/reviews.html', restaurant=current_r, reviews=r_reviews)

@restaurant_bp.route('/analytics')
@role_required('restaurant', 'admin')
def analytics():
    """Restaurant revenue and order analytics."""
    current_r = get_current_restaurant()
    r_orders = [o for o in get_all_orders() if o['restaurant_id'] == current_r['id']]
    
    # Calculate revenue trends
    total_sales = sum(o['total'] for o in r_orders)
    avg_order_val = (total_sales / len(r_orders)) if r_orders else 0.0

    return render_template(
        'restaurant/analytics.html',
        restaurant=current_r,
        orders=r_orders,
        total_sales=total_sales,
        avg_order_val=avg_order_val
    )

# Feature Dashboards: Restaurant Owner Kitchen Fulfillment & Analytics
