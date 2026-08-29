"""Customer Blueprint handling browsing, cart, checkout, orders, and live tracking."""
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
    """Food detail endpoint."""
    food = next((f for f in FOODS if f['id'] == food_id), None)
    if not food:
        return jsonify({'error': 'Food item not found'}), 404

    restaurant = next((r for r in RESTAURANTS if r['id'] == food['restaurant_id']), None)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('customer/food_modal.html', food=food, restaurant=restaurant)

    return jsonify({
        'food': food,
        'restaurant_name': restaurant['name'] if restaurant else ''
    })

@customer_bp.route('/category/<slug>')
def category_detail(slug):
    """Category detail page."""
    cat = next((c for c in CATEGORIES if c['slug'] == slug or c['name'].lower() == slug.lower()), None)
    if not cat:
        abort(404)

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
    food_id = int(data.get('food_id', 0))
    quantity = int(data.get('quantity', 1))
    variant = data.get('variant', '')
    variant_price = float(data.get('variant_price', 0.0))

    food = next((f for f in FOODS if f['id'] == food_id), None)
    if not food:
        return jsonify({'success': False, 'message': 'Food item not found.'}), 404

    cart = session.get('cart', [])

    if cart and cart[0].get('restaurant_id') != food['restaurant_id']:
        cart = []
        session.pop('applied_coupon', None)
        flash("Your cart was reset because items can only be ordered from one restaurant at a time.", "warning")

    existing_item = None
    for item in cart:
        if item['food_id'] == food_id and item.get('variant') == variant:
            existing_item = item
            break

    if existing_item:
        existing_item['quantity'] += quantity
    else:
        cart.append({
            'food_id': food['id'],
            'restaurant_id': food['restaurant_id'],
            'name': food['name'],
            'image': food['image'],
            'price': food['discount_price'],
            'original_price': food['price'],
            'variant': variant,
            'variant_price': variant_price,
            'add_ons': [],
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


# --- CHECKOUT & ORDER CREATION ROUTES ---

@customer_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Checkout page supporting simulated COD, Card, and UPI payments."""
    cart = session.get('cart', [])
    if not cart:
        flash("Your cart is empty. Add some delicious dishes before checkout!", "warning")
        return redirect(url_for('customer.restaurants'))

    current_user = session.get('user')
    if not current_user:
        flash("Please sign in or use a demo login to proceed with checkout.", "warning")
        return redirect(url_for('auth.login'))

    totals = calculate_cart_totals(cart, coupon_code=session.get('applied_coupon'))

    restaurant_id = cart[0]['restaurant_id']
    restaurant = next((r for r in RESTAURANTS if r['id'] == restaurant_id), None)

    if request.method == 'POST':
        delivery_address = request.form.get('address', '').strip()
        phone = request.form.get('phone', '').strip()
        payment_method = request.form.get('payment_method', 'Cash on Delivery')
        special_instructions = request.form.get('special_instructions', '').strip()

        if not delivery_address or not phone:
            flash("Delivery address and contact phone number are required.", "danger")
            return render_template('customer/checkout.html', cart=cart, totals=totals, restaurant=restaurant)

        new_id = len(ORDERS) + 1001
        order_num = f"ORD-2026-{random.randint(1000, 9999)}"
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_short = datetime.datetime.now().strftime("%H:%M")

        new_order = {
            "id": new_id,
            "order_number": order_num,
            "customer_id": current_user['id'],
            "customer_name": current_user['name'],
            "customer_phone": phone,
            "restaurant_id": restaurant_id,
            "restaurant_name": restaurant['name'] if restaurant else 'FoodFlow Kitchen',
            "delivery_agent_id": 1,
            "items": list(cart),
            "subtotal": totals['subtotal'],
            "discount": totals['discount'],
            "coupon_code": totals['coupon_code'],
            "delivery_fee": totals['delivery_fee'],
            "tax": totals['tax'],
            "total": totals['final_total'],
            "status": "Order Placed",
            "payment_method": payment_method,
            "payment_status": "Paid" if payment_method != 'Cash on Delivery' else 'Pending (COD)',
            "delivery_address": delivery_address,
            "special_instructions": special_instructions,
            "created_at": now_str,
            "status_history": [
                {"status": "Order Placed", "time": time_short}
            ]
        }

        add_order(new_order)

        session['cart'] = []
        session.pop('applied_coupon', None)
        session.modified = True

        flash(f"Order #{order_num} placed successfully! 🎉", "success")
        return redirect(url_for('customer.order_confirmation', order_id=new_id))

    return render_template('customer/checkout.html', cart=cart, totals=totals, restaurant=restaurant)

@customer_bp.route('/order-confirmation/<order_id>')
def order_confirmation(order_id):
    """Order confirmation screen after successful checkout."""
    order = get_order_by_id(order_id)
    if not order:
        abort(404)

    return render_template('customer/order_confirmation.html', order=order)


# --- ORDER SYSTEM & LIVE TRACKING ROUTES ---

@customer_bp.route('/orders')
@login_required
def order_history():
    """Customer order history page."""
    current_user_id = session['user']['id']
    all_orders = get_all_orders()
    
    # Filter orders for current user (or show all seed orders if demo customer)
    user_orders = [o for o in all_orders if str(o.get('customer_id')) == str(current_user_id)]
    if not user_orders:
        user_orders = all_orders  # Fallback so user always sees sample orders

    return render_template('customer/orders.html', orders=user_orders)

@customer_bp.route('/order/<order_id>')
@login_required
def order_details(order_id):
    """Order details view."""
    order = get_order_by_id(order_id)
    if not order:
        abort(404)

    return render_template('customer/order_details.html', order=order)

@customer_bp.route('/order-tracking/<order_id>')
def order_tracking(order_id):
    """Simulated live order tracking view with progress stepper."""
    order = get_order_by_id(order_id)
    if not order:
        abort(404)

    # Order tracking step milestones
    tracking_steps = [
        {"key": "Order Placed", "title": "Order Placed", "desc": "We have received your order", "icon": "📝"},
        {"key": "Confirmed", "title": "Restaurant Confirmed", "desc": "Kitchen accepted your order", "icon": "👨‍🍳"},
        {"key": "Preparing", "title": "Preparing Food", "desc": "Chef is cooking your meal", "icon": "🍳"},
        {"key": "Ready for Pickup", "title": "Ready for Pickup", "desc": "Food is packed & ready", "icon": "🛍️"},
        {"key": "Out for Delivery", "title": "Out for Delivery", "desc": "Delivery partner picked up food", "icon": "🛵"},
        {"key": "Delivered", "title": "Delivered", "desc": "Enjoy your delicious meal!", "icon": "😋"}
    ]

    # Calculate active step index
    status_order_map = {
        "Order Placed": 0,
        "Confirmed": 1,
        "Preparing": 2,
        "Ready for Pickup": 3,
        "Out for Delivery": 4,
        "Delivered": 5,
        "Cancelled": -1
    }
    
    active_index = status_order_map.get(order["status"], 0)

    return render_template(
        'customer/order_tracking.html',
        order=order,
        tracking_steps=tracking_steps,
        active_index=active_index
    )

@customer_bp.route('/order/cancel/<order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    """Cancel eligible order."""
    order = get_order_by_id(order_id)
    if not order:
        abort(404)

    if order['status'] in ['Order Placed', 'Confirmed']:
        update_order_status(order_id, 'Cancelled')
        flash(f"Order #{order['order_number']} has been cancelled.", "info")
    else:
        flash("Order cannot be cancelled as kitchen preparation has already begun.", "danger")

    return redirect(url_for('customer.order_details', order_id=order_id))

@customer_bp.route('/order/reorder/<order_id>', methods=['POST'])
@login_required
def reorder(order_id):
    """Copy past order items back into active session cart."""
    order = get_order_by_id(order_id)
    if not order:
        abort(404)

    session['cart'] = list(order['items'])
    session.modified = True

    flash(f"Items from Order #{order['order_number']} added to your cart!", "success")
    return redirect(url_for('customer.view_cart'))


# --- WISHLIST, ADDRESSES & OFFERS ROUTES ---

@customer_bp.route('/favorites')
def view_favorites():
    """Customer saved favorites wishlist page."""
    return render_template('customer/favorites.html')

@customer_bp.route('/addresses')
def view_addresses():
    """Customer saved delivery address manager."""
    return render_template('customer/addresses.html')

@customer_bp.route('/offers')
def view_offers():
    """Customer promo offers storefront."""
    return render_template('customer/offers.html', offers=OFFERS)


# Feature Catalog: Multi-City Restaurant Directory & Catalog Search
