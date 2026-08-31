"""Delivery Partner Blueprint for managing active deliveries, order status steps, and earnings."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from data.delivery import DELIVERY_PARTNERS
from data.orders import ORDERS, get_all_orders, get_order_by_id, update_order_status
from data.restaurants import RESTAURANTS
from utils.decorators import role_required

delivery_bp = Blueprint('delivery', __name__, url_prefix='/delivery')

def get_current_driver():
    """Helper to get delivery partner details for logged in user."""
    user = session.get('user', {})
    driver_id = user.get('id', 1)
    driver = next((d for d in DELIVERY_PARTNERS if d['id'] == driver_id), DELIVERY_PARTNERS[0])
    return driver

@delivery_bp.route('/dashboard')
@role_required('delivery', 'admin')
def dashboard():
    """Delivery partner overview dashboard."""
    driver = get_current_driver()
    all_orders = get_all_orders()

    # Active delivery order
    active_order = None
    if driver.get('active_order_id'):
        active_order = get_order_by_id(driver['active_order_id'])
    
    if not active_order:
        # Fallback to any order marked 'Out for Delivery' or 'Ready for Pickup'
        active_order = next((o for o in all_orders if o['status'] in ['Ready for Pickup', 'Out for Delivery']), None)

    # Completed deliveries
    completed_orders = [o for o in all_orders if o['status'] == 'Delivered']

    metrics = {
        "earnings_today": driver['earnings_today'],
        "total_earnings": driver['total_earnings'],
        "total_deliveries": driver['total_deliveries'],
        "rating": driver['rating'],
        "status": driver['status']
    }

    # Available orders to accept
    available_orders = [o for o in all_orders if o['status'] in ['Confirmed', 'Preparing', 'Ready for Pickup']]

    return render_template(
        'delivery/dashboard.html',
        driver=driver,
        metrics=metrics,
        active_order=active_order,
        available_orders=available_orders,
        completed_orders=completed_orders
    )

@delivery_bp.route('/accept/<order_id>', methods=['POST'])
@role_required('delivery', 'admin')
def accept_delivery(order_id):
    """Accept an assigned order for pickup and delivery."""
    order = get_order_by_id(order_id)
    if not order:
        flash("Order not found.", "danger")
        return redirect(url_for('delivery.dashboard'))

    driver = get_current_driver()
    driver['active_order_id'] = order['id']
    
    if order['status'] in ['Confirmed', 'Preparing']:
        update_order_status(order_id, 'Ready for Pickup')

    flash(f"Order #{order.get('order_number')} accepted for delivery!", "success")
    return redirect(url_for('delivery.active_delivery'))

@delivery_bp.route('/active')
@role_required('delivery', 'admin')
def active_delivery():
    """Active delivery detail view with step-by-step progress controls."""
    driver = get_current_driver()
    all_orders = get_all_orders()

    active_order = None
    if driver.get('active_order_id'):
        active_order = get_order_by_id(driver['active_order_id'])

    if not active_order:
        active_order = next((o for o in all_orders if o['status'] in ['Ready for Pickup', 'Out for Delivery']), None)

    if not active_order and all_orders:
        active_order = all_orders[0]

    restaurant = None
    if active_order:
        restaurant = next((r for r in RESTAURANTS if r['id'] == active_order['restaurant_id']), None)

    # Step progress milestones
    delivery_milestones = [
        {"status": "Confirmed", "label": "Order Confirmed by Restaurant", "icon": "📝"},
        {"status": "Preparing", "label": "Preparing in Kitchen", "icon": "🍳"},
        {"status": "Ready for Pickup", "label": "Arrived at Restaurant", "icon": "🏬"},
        {"status": "Out for Delivery", "label": "Picked Up & Out for Delivery", "icon": "🛵"},
        {"status": "Delivered", "label": "Delivered to Customer", "icon": "✅"}
    ]

    return render_template(
        'delivery/active.html',
        driver=driver,
        order=active_order,
        restaurant=restaurant,
        milestones=delivery_milestones
    )

@delivery_bp.route('/update-status/<order_id>', methods=['POST'])
@role_required('delivery', 'admin')
def update_delivery_status(order_id):
    """Progress active delivery to next step."""
    new_status = request.form.get('status')
    if order_id and new_status:
        success, msg = update_order_status(order_id, new_status)
        if not success:
            flash(msg, "danger")
            return redirect(url_for('delivery.active_delivery'))

        driver = get_current_driver()
        if new_status == 'Delivered':
            driver['earnings_today'] += 50.0
            driver['total_earnings'] += 50.0
            driver['total_deliveries'] += 1
            driver['active_order_id'] = None
            flash(f"Delivery completed! ₹50.00 added to your earnings.", "success")
            return redirect(url_for('delivery.dashboard'))

        flash(f"Delivery status updated to '{new_status}'.", "info")

    return redirect(url_for('delivery.active_delivery'))

@delivery_bp.route('/earnings')
@role_required('delivery', 'admin')
def earnings():
    """Earnings summary and payout breakdown."""
    driver = get_current_driver()
    all_orders = get_all_orders()
    completed = [o for o in all_orders if o['status'] == 'Delivered']

    return render_template('delivery/earnings.html', driver=driver, completed_orders=completed)

@delivery_bp.route('/history')
@role_required('delivery', 'admin')
def history():
    """Completed delivery history log."""
    driver = get_current_driver()
    all_orders = get_all_orders()
    completed = [o for o in all_orders if o['status'] == 'Delivered']

    return render_template('delivery/history.html', driver=driver, orders=completed)
