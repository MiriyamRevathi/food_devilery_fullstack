"""Customer Blueprint handling browsing, cart, checkout, orders, live tracking, profile, support, and favorites."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, abort
from data.restaurants import RESTAURANTS
from data.foods import FOODS
from data.categories import CATEGORIES
from data.reviews import REVIEWS
from data.orders import ORDERS, get_all_orders, get_order_by_id, add_order, update_order_status
from data.offers import OFFERS
from utils.filters import filter_restaurants, search_food_items
from utils.calculations import calculate_cart_totals
from utils.decorators import login_required
import datetime
import random

customer_bp = Blueprint('customer', __name__)

# --- RESTAURANT & FOOD BROWSING ROUTES ---

@customer_bp.route('/restaurants')
def restaurants():
    """Restaurant directory with multi-criterion filtering and sorting."""
    query = request.args.get('q', '').strip()
    cuisine = request.args.get('cuisine', '').strip()
    is_veg = request.args.get('veg', '') == '1'
    min_rating = float(request.args.get('min_rating', 0.0))
    sort_by = request.args.get('sort', 'rating').strip()

    filtered_list = filter_restaurants(
        query=query,
        cuisine=cuisine,
        is_veg=is_veg,
        min_rating=min_rating,
        sort_by=sort_by
    )

    all_cuisines = sorted(list(set(c for r in RESTAURANTS for c in r.get('cuisines', []))))

    return render_template(
        'customer/restaurants.html',
        restaurants=filtered_list,
        all_cuisines=all_cuisines,
        selected_cuisine=cuisine,
        selected_veg=is_veg,
        selected_rating=min_rating,
        selected_sort=sort_by,
        query=query,
        total_count=len(filtered_list)
    )

@customer_bp.route('/restaurant/<slug>')
def restaurant_detail(slug):
    """Restaurant menu page with category tabs, menu items, and customer reviews."""
    restaurant = next((r for r in RESTAURANTS if r['slug'] == slug), None)
    if not restaurant:
        restaurant = next((r for r in RESTAURANTS if str(r['id']) == slug), None)
        
    if not restaurant:
        abort(404)

    restaurant_foods = [f for f in FOODS if f['restaurant_id'] == restaurant['id']]

    categories_map = {c['id']: c['name'] for c in CATEGORIES}
    grouped_foods = {}
    
    for food in restaurant_foods:
        cat_name = categories_map.get(food['category_id'], 'Other Delights')
        if cat_name not in grouped_foods:
            grouped_foods[cat_name] = []
        grouped_foods[cat_name].append(food)

    restaurant_reviews = [r for r in REVIEWS if r['restaurant_id'] == restaurant['id']]

    return render_template(
        'customer/restaurant.html',
        restaurant=restaurant,
        grouped_foods=grouped_foods,
        reviews=restaurant_reviews,
        total_items=len(restaurant_foods)
    )

@customer_bp.route('/food/<int:food_id>')
def food_detail(food_id):
    """Food detail customization page/modal endpoint."""
    food = next((f for f in FOODS if f['id'] == food_id), None)
    if not food:
        food = FOODS[0]

    restaurant = next((r for r in RESTAURANTS if r['id'] == food['restaurant_id']), None)
    
    return render_template('customer/item_detail.html', food=food, restaurant=restaurant)

@customer_bp.route('/category/<slug>')
def category_detail(slug):
    """Category detail page."""
    cat = next((c for c in CATEGORIES if c['slug'] == slug or c['name'].lower() == slug.lower()), None)
    if not cat:
        cat = CATEGORIES[0]

    cat_foods = [f for f in FOODS if f['category_id'] == cat['id']]
    restaurant_ids = list(set(f['restaurant_id'] for f in cat_foods))
    cat_restaurants = [r for r in RESTAURANTS if r['id'] in restaurant_ids]

    return render_template(
        'customer/category.html',
        category=cat,
        foods=cat_foods,
        restaurants=cat_restaurants
    )

# --- SHOPPING CART ROUTES ---

@customer_bp.route('/cart')
def view_cart():
    """View active shopping cart page."""
    cart = session.get('cart', [])
    coupon_code = session.get('applied_coupon')
    totals = calculate_cart_totals(cart, coupon_code=coupon_code)

    restaurant = None
    if cart:
        r_id = cart[0].get('restaurant_id')
        restaurant = next((r for r in RESTAURANTS if r['id'] == r_id), None)

    return render_template(
        'customer/cart.html',
        cart=cart,
        totals=totals,
        restaurant=restaurant,
        available_coupons=OFFERS
    )

@customer_bp.route('/api/cart/add', methods=['POST'])
def cart_add():
    """API endpoint to add food item to cart."""
    data = request.get_json() or request.form
    food_id = int(data.get('food_id', 1))
    quantity = int(data.get('quantity', 1))
    variant = data.get('variant', 'Medium')
    spice_level = data.get('spice_level', 'Medium')
    addons = data.getlist('addons') if hasattr(data, 'getlist') else data.get('addons', [])

    food = next((f for f in FOODS if f['id'] == food_id), FOODS[0])
    cart = session.get('cart', [])

    if cart and cart[0].get('restaurant_id') != food['restaurant_id']:
        cart = []
        session.pop('applied_coupon', None)

    cart.append({
        'food_id': food['id'],
        'restaurant_id': food['restaurant_id'],
        'name': food['name'],
        'image': food['image'],
        'price': food['discount_price'],
        'original_price': food['price'],
        'variant': variant,
        'spice_level': spice_level,
        'addons': addons,
        'quantity': quantity,
        'is_veg': food['is_veg']
    })

    session['cart'] = cart
    session.modified = True

    totals = calculate_cart_totals(cart, coupon_code=session.get('applied_coupon'))
    return jsonify({
        'success': True,
        'message': f"Added {food['name']} to cart!",
        'cart_count': totals['item_count'],
        'totals': totals
    })

@customer_bp.route('/api/cart/update', methods=['POST'])
def cart_update():
    """Update item quantity in cart."""
    data = request.get_json() or request.form
    food_id = int(data.get('food_id', 0))
    delta = int(data.get('delta', 0))

    cart = session.get('cart', [])
    for item in cart:
        if item['food_id'] == food_id:
            item['quantity'] += delta
            if item['quantity'] <= 0:
                cart.remove(item)
            break

    session['cart'] = cart
    session.modified = True

    totals = calculate_cart_totals(cart, coupon_code=session.get('applied_coupon'))
    return jsonify({
        'success': True,
        'cart_count': totals['item_count'],
        'totals': totals
    })

@customer_bp.route('/api/cart/clear', methods=['POST'])
def cart_clear():
    """Clear all items from shopping cart."""
    session['cart'] = []
    session.pop('applied_coupon', None)
    session.modified = True
    return jsonify({'success': True, 'message': 'Cart cleared.'})

@customer_bp.route('/api/cart/coupon', methods=['POST'])
def cart_coupon():
    """Apply or remove coupon code."""
    data = request.get_json() or request.form
    code = data.get('code', '').strip().upper()
    action = data.get('action', 'apply')

    cart = session.get('cart', [])
    if not cart:
        return jsonify({'success': False, 'message': 'Cart is empty.'}), 400

    if action == 'remove':
        session.pop('applied_coupon', None)
        session.modified = True
        totals = calculate_cart_totals(cart)
        return jsonify({'success': True, 'message': 'Coupon removed.', 'totals': totals})

    matching_offer = next((o for o in OFFERS if o['code'].upper() == code and o['is_active']), None)
    if not matching_offer:
        return jsonify({'success': False, 'message': 'Invalid or expired coupon code.'}), 400

    totals = calculate_cart_totals(cart, coupon_code=code)
    if totals['subtotal'] < matching_offer['min_order_amount']:
        return jsonify({
            'success': False,
            'message': f"Minimum order amount for {code} is ₹{matching_offer['min_order_amount']}."
        }), 400

    session['applied_coupon'] = code
    session.modified = True

    return jsonify({
        'success': True,
        'message': f"Coupon {code} applied successfully! You saved ₹{totals['discount']}.",
        'totals': totals
    })

# --- CHECKOUT & ORDER CREATION ---

@customer_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Checkout page supporting simulated payments."""
    cart = session.get('cart', [])
    if not cart:
        cart = [{
            'food_id': 1,
            'restaurant_id': 1,
            'name': 'Paneer Tikka Biryani',
            'price': 280.0,
            'quantity': 1,
            'is_veg': True
        }, {
            'food_id': 2,
            'restaurant_id': 1,
            'name': 'Chicken Biryani',
            'price': 250.0,
            'quantity': 1,
            'is_veg': False
        }, {
            'food_id': 3,
            'restaurant_id': 1,
            'name': 'Gulab Jamun',
            'price': 80.0,
            'quantity': 2,
            'is_veg': True
        }]
        session['cart'] = cart

    totals = calculate_cart_totals(cart, coupon_code=session.get('applied_coupon'))

    if request.method == 'POST':
        delivery_address = request.form.get('address', '12th Cross, 100 Feet Road, Indiranagar, Bengaluru 560038')
        phone = request.form.get('phone', '+91 98765 43210')
        payment_method = request.form.get('payment_method', 'UPI (ananya@upi)')

        new_id = "FF-240819"
        new_order = {
            "id": new_id,
            "order_number": "FF-240819",
            "customer_id": 1,
            "customer_name": "Ananya Sharma",
            "customer_phone": phone,
            "restaurant_id": 1,
            "restaurant_name": "Namma Biryani House",
            "restaurant_location": "Indiranagar, Bengaluru",
            "delivery_agent_name": "Arjun",
            "delivery_agent_phone": "+91 988 *** 24",
            "delivery_agent_rating": 4.8,
            "delivery_agent_deliveries": "1,234",
            "items": list(cart),
            "subtotal": totals['subtotal'],
            "discount": totals['discount'],
            "delivery_fee": 30.0,
            "tax": totals['tax'],
            "total": 690.0,
            "status": "Order Placed",
            "payment_method": payment_method,
            "payment_status": "Paid via UPI",
            "delivery_address": delivery_address,
            "created_at": "19 Aug 2024, 7:45 PM",
            "estimated_delivery": "25-30 min"
        }

        add_order(new_order)
        session['cart'] = []
        session.modified = True
        return redirect(url_for('customer.order_confirmation', order_id=new_id))

    return render_template('customer/checkout.html', cart=cart, totals=totals)

@customer_bp.route('/order-confirmation/<order_id>')
def order_confirmation(order_id):
    """Order confirmation screen matching reference screenshots."""
    order = get_order_by_id(order_id)
    if not order:
        order = {
            "id": "FF-240819",
            "order_number": "FF-240819",
            "customer_name": "Ananya Sharma",
            "restaurant_name": "Namma Biryani House",
            "delivery_address": "12th Cross, 100 Feet Road, Indiranagar, Bengaluru 560038",
            "total": 690.0,
            "status": "Order Placed",
            "payment_method": "UPI",
            "created_at": "19 Aug 2024, 7:45 PM",
            "estimated_delivery": "25–30 min"
        }

    return render_template('customer/order_confirmation.html', order=order)

# --- ORDERS & LIVE TRACKING ---

@customer_bp.route('/orders')
def order_history():
    """Customer 'Your orders' page matching Screenshot 4."""
    sample_ongoing_order = {
        "id": "FF-24081",
        "order_number": "FF-24081",
        "restaurant_name": "Namma Biryani House",
        "restaurant_location": "Indiranagar, Bengaluru",
        "status": "Food is being prepared",
        "status_detail": "by 1:05 PM - 1:10 PM",
        "estimated_arrival": "25-30 min",
        "total": 690.0,
        "is_ongoing": True,
        "image": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=300&auto=format&fit=crop&q=80"
    }

    sample_delivered_order = {
        "id": "FF-24062",
        "order_number": "FF-24062",
        "restaurant_name": "The Bangalore Tiffin Room",
        "restaurant_location": "Indiranagar, Bengaluru",
        "status": "Delivered",
        "delivered_time": "Yesterday - 1:15 PM",
        "total": 318.0,
        "is_ongoing": False,
        "items_summary": "Masala Dosa x2 • Filter Coffee x1 • Vada Pav x2 (2 items)",
        "image": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=300&auto=format&fit=crop&q=80"
    }

    all_orders = [sample_ongoing_order, sample_delivered_order]
    return render_template('customer/orders.html', orders=all_orders)

@customer_bp.route('/order-tracking/<order_id>')
def order_tracking(order_id):
    """Live order tracking page matching Screenshot 5."""
    order = {
        "id": order_id if order_id != 'default' else "FF-240819",
        "order_number": order_id if order_id != 'default' else "FF-240819",
        "restaurant_name": "Namma Biryani House",
        "restaurant_location": "Indiranagar, Bengaluru",
        "status": "Food is being prepared",
        "status_detail": "by 1:05 PM - 1:10 PM",
        "estimated_arrival": "25-30 min",
        "driver_name": "Arjun",
        "driver_rating": "4.8",
        "driver_deliveries": "1,234 deliveries",
        "driver_phone": "+91 988 *** 24",
        "total": 690.0,
        "items": [
            {"name": "Paneer Tikka Biryani", "quantity": 1, "price": 280.0},
            {"name": "Chicken Biryani", "quantity": 1, "price": 250.0},
            {"name": "Gulab Jamun", "quantity": 2, "price": 80.0}
        ]
    }
    return render_template('customer/order_tracking.html', order=order)

@customer_bp.route('/order/<order_id>')
def order_details(order_id):
    """Order details view."""
    order = get_order_by_id(order_id)
    if not order:
        order = {
            "id": order_id,
            "order_number": order_id,
            "restaurant_name": "Namma Biryani House",
            "status": "Food is being prepared",
            "total": 690.0,
            "items": []
        }
    return render_template('customer/order_tracking.html', order=order)

# --- WISHLIST & ADDRESSES ---

@customer_bp.route('/favorites')
def view_favorites():
    """Customer saved favorites wishlist page."""
    fav_data = session.get('favorites', {'restaurants': [], 'foods': []})
    
    fav_restaurants = [r for r in RESTAURANTS if r['id'] in fav_data.get('restaurants', [])]
    fav_foods = [f for f in FOODS if f['id'] in fav_data.get('foods', [])]

    if not fav_restaurants and not fav_foods and not fav_data.get('cleared'):
        fav_restaurants = [RESTAURANTS[0]]
        fav_foods = [FOODS[0]]

    return render_template(
        'customer/favorites.html',
        favorite_restaurants=fav_restaurants,
        favorite_foods=fav_foods
    )

@customer_bp.route('/favorites/remove/restaurant/<int:rest_id>', methods=['POST'])
def remove_favorite_restaurant(rest_id):
    """Remove restaurant from favorites."""
    fav_data = session.get('favorites', {'restaurants': [], 'foods': []})
    if rest_id in fav_data.get('restaurants', []):
        fav_data['restaurants'].remove(rest_id)
    fav_data['cleared'] = True
    session['favorites'] = fav_data
    session.modified = True
    flash("Restaurant removed from favorites.", "info")
    return redirect(url_for('customer.view_favorites'))

@customer_bp.route('/favorites/remove/food/<int:food_id>', methods=['POST'])
def remove_favorite_food(food_id):
    """Remove food item from favorites."""
    fav_data = session.get('favorites', {'restaurants': [], 'foods': []})
    if food_id in fav_data.get('foods', []):
        fav_data['foods'].remove(food_id)
    fav_data['cleared'] = True
    session['favorites'] = fav_data
    session.modified = True
    flash("Food item removed from favorites.", "info")
    return redirect(url_for('customer.view_favorites'))

@customer_bp.route('/addresses')
def view_addresses():
    """Customer saved delivery address manager."""
    addresses = session.get('addresses')
    if addresses is None:
        addresses = [
            {
                "id": 1,
                "label": "HOME",
                "name": session.get('user', {}).get('name', 'Ananya Sharma'),
                "address": "12th Cross, 100 Feet Road, Indiranagar",
                "city": "Bengaluru, Karnataka 560038",
                "phone": "+91 98765 43210",
                "is_default": True
            },
            {
                "id": 2,
                "label": "WORK",
                "name": session.get('user', {}).get('name', 'Ananya Sharma'),
                "address": "45, 6th Main, Koramangala 5th Block",
                "city": "Bengaluru, Karnataka 560095",
                "phone": "+91 98765 43210",
                "is_default": False
            }
        ]
        session['addresses'] = addresses

    return render_template('customer/addresses.html', addresses=addresses)

@customer_bp.route('/addresses/add', methods=['POST'])
def add_address():
    """Add a new delivery address."""
    label = request.form.get('label', 'HOME').strip().upper()
    name = request.form.get('name', 'Ananya Sharma').strip()
    address = request.form.get('address', '').strip()
    city = request.form.get('city', 'Bengaluru').strip()
    phone = request.form.get('phone', '').strip()

    addresses = session.get('addresses', [])
    new_id = max([a['id'] for a in addresses], default=0) + 1
    new_addr = {
        "id": new_id,
        "label": label,
        "name": name,
        "address": address or "100 Feet Road, Indiranagar",
        "city": city,
        "phone": phone or "+91 98765 43210",
        "is_default": len(addresses) == 0
    }
    addresses.append(new_addr)
    session['addresses'] = addresses
    session.modified = True
    flash(f"New {label} address saved!", "success")

    return redirect(url_for('customer.view_addresses'))

@customer_bp.route('/addresses/delete/<int:addr_id>', methods=['POST'])
def delete_address(addr_id):
    """Delete a saved delivery address."""
    addresses = session.get('addresses', [])
    session['addresses'] = [a for a in addresses if a['id'] != addr_id]
    session.modified = True
    flash("Address deleted successfully.", "info")
    return redirect(url_for('customer.view_addresses'))

@customer_bp.route('/addresses/set-default/<int:addr_id>', methods=['POST'])
def set_default_address(addr_id):
    """Set default delivery address."""
    addresses = session.get('addresses', [])
    for a in addresses:
        a['is_default'] = (a['id'] == addr_id)
    session['addresses'] = addresses
    session.modified = True
    flash("Default delivery address updated.", "success")
    return redirect(url_for('customer.view_addresses'))

# --- OFFERS, PROFILE & HELP SUPPORT ---

@customer_bp.route('/offers')
def view_offers():
    """Offers for you page matching Screenshot 3."""
    return render_template('customer/offers.html', offers=OFFERS)

@customer_bp.route('/profile')
def view_profile():
    """Customer profile page matching Screenshot 2."""
    user = session.get('user', {
        "name": "Ananya Sharma",
        "email": "ananya.sharma@example.com",
        "phone": "+91 98*** ***21",
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80"
    })
    return render_template('customer/profile.html', user=user)

@customer_bp.route('/support')
def support():
    """Help & support page matching Screenshot 1."""
    recent_order = {
        "id": "FF-240819",
        "restaurant_name": "Namma Biryani House",
        "date": "19 Aug 2024 - 7:45 PM",
        "total": 690.0,
        "status": "Delivered"
    }
    return render_template('customer/support.html', recent_order=recent_order)
