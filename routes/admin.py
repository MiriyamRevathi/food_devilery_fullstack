"""Admin Control Panel Blueprint for system-wide management and analytics reports."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from data.users import USERS
from data.restaurants import RESTAURANTS
from data.foods import FOODS
from data.orders import ORDERS, get_all_orders, get_order_by_id, update_order_status
from data.offers import OFFERS
from data.reviews import REVIEWS
from data.cities import CITIES
from utils.decorators import role_required
import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@role_required('admin')
def dashboard():
    """Admin control panel overview dashboard."""
    all_orders = get_all_orders()
    total_revenue = sum(o['total'] for o in all_orders if o['status'] != 'Cancelled')

    pending_orders = len([o for o in all_orders if o['status'] in ['Order Placed', 'Confirmed', 'Preparing', 'Ready for Pickup', 'Out for Delivery']])
    completed_orders = len([o for o in all_orders if o['status'] == 'Delivered'])
    cancelled_orders = len([o for o in all_orders if o['status'] == 'Cancelled'])

    metrics = {
        "total_users": len(USERS),
        "total_restaurants": len(RESTAURANTS),
        "total_foods": len(FOODS),
        "total_orders": len(all_orders),
        "total_revenue": total_revenue,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "cancelled_orders": cancelled_orders
    }

    return render_template(
        'admin/dashboard.html',
        metrics=metrics,
        recent_users=USERS[:5],
        recent_orders=all_orders[:5],
        restaurants=RESTAURANTS[:5]
    )

@admin_bp.route('/users')
@role_required('admin')
def users():
    """Manage user accounts."""
    role_filter = request.args.get('role', '').strip()
    search_q = request.args.get('q', '').strip().lower()

    filtered_users = list(USERS)
    if role_filter:
        filtered_users = [u for u in filtered_users if u['role'] == role_filter]

    if search_q:
        filtered_users = [u for u in filtered_users if search_q in u['name'].lower() or search_q in u['email'].lower()]

    return render_template(
        'admin/users.html',
        users=filtered_users,
        selected_role=role_filter,
        search_q=search_q
    )

@admin_bp.route('/user/toggle/<int:user_id>', methods=['POST'])
@role_required('admin')
def toggle_user(user_id):
    """Enable or disable user account."""
    target = next((u for u in USERS if u['id'] == user_id), None)
    if target:
        target['is_active'] = not target.get('is_active', True)
        status = "enabled" if target['is_active'] else "disabled"
        flash(f"User account '{target['email']}' has been {status}.", "info")
    else:
        flash("User not found.", "warning")
    return redirect(url_for('admin.users'))

@admin_bp.route('/restaurants', methods=['GET', 'POST'])
@role_required('admin')
def restaurants():
    """Manage restaurant listings."""
    if request.method == 'POST':
        restaurant_id = int(request.form.get('restaurant_id', 0))
        action = request.form.get('action')

        target = next((r for r in RESTAURANTS if r['id'] == restaurant_id), None)
        if target:
            if action == 'toggle_open':
                target['is_open'] = not target.get('is_open', True)
                flash(f"Restaurant '{target['name']}' status set to {'Open' if target['is_open'] else 'Closed'}.", "info")
            elif action == 'toggle_featured':
                target['is_featured'] = not target.get('is_featured', False)
                flash(f"Restaurant '{target['name']}' featured status updated.", "info")

        return redirect(url_for('admin.restaurants'))

    return render_template('admin/restaurants.html', restaurants=RESTAURANTS)

@admin_bp.route('/foods')
@role_required('admin')
def foods():
    """Global food catalog audit."""
    return render_template('admin/foods.html', foods=FOODS)

@admin_bp.route('/orders', methods=['GET', 'POST'])
@role_required('admin')
def orders():
    """Global order control center."""
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        new_status = request.form.get('status')
        if order_id and new_status:
            success, msg = update_order_status(order_id, new_status, is_admin=True)
            if success:
                flash(f"Admin override: Order #{order_id} status changed to '{new_status}'.", "success")
            else:
                flash(msg, "danger")
            return redirect(url_for('admin.orders'))

    all_orders = get_all_orders()
    status_filter = request.args.get('status', '').strip()
    if status_filter:
        all_orders = [o for o in all_orders if o['status'] == status_filter]

    return render_template('admin/orders.html', orders=all_orders, selected_status=status_filter)

@admin_bp.route('/offers', methods=['GET', 'POST'])
@role_required('admin')
def offers():
    """Manage promo coupons."""
    if request.method == 'POST':
        code = request.form.get('code', '').strip().upper()
        discount_type = request.form.get('discount_type', 'percentage')
        discount_value = float(request.form.get('discount_value', 0.0))
        min_order = float(request.form.get('min_order_amount', 0.0))
        max_discount = float(request.form.get('max_discount_amount', 100.0))
        description = request.form.get('description', '').strip()

        if code and discount_value > 0:
            new_offer = {
                "code": code,
                "discount_type": discount_type,
                "discount_value": discount_value,
                "min_order_amount": min_order,
                "max_discount_amount": max_discount,
                "valid_until": "2026-12-31",
                "is_active": True,
                "description": description,
                "badge": "Admin Created"
            }
            OFFERS.append(new_offer)
            flash(f"Promo coupon {code} created!", "success")
            return redirect(url_for('admin.offers'))

    return render_template('admin/offers.html', offers=OFFERS)

@admin_bp.route('/offers/delete/<code>', methods=['POST'])
@role_required('admin')
def delete_offer(code):
    """Delete a promo coupon code."""
    global OFFERS
    code_upper = code.strip().upper()
    target = next((o for o in OFFERS if o['code'].upper() == code_upper), None)
    if target:
        OFFERS.remove(target)
        flash(f"Promo coupon {code_upper} deleted.", "info")
    else:
        flash("Promo code not found.", "warning")
    return redirect(url_for('admin.offers'))

@admin_bp.route('/reports')
@role_required('admin')
def reports():
    """Analytics reports featuring pure JS/CSS interactive charts."""
    all_orders = get_all_orders()
    total_sales = sum(o['total'] for o in all_orders if o['status'] != 'Cancelled')

    status_counts = {
        "Order Placed": len([o for o in all_orders if o['status'] == 'Order Placed']),
        "Confirmed": len([o for o in all_orders if o['status'] == 'Confirmed']),
        "Preparing": len([o for o in all_orders if o['status'] == 'Preparing']),
        "Out for Delivery": len([o for o in all_orders if o['status'] == 'Out for Delivery']),
        "Delivered": len([o for o in all_orders if o['status'] == 'Delivered']),
        "Cancelled": len([o for o in all_orders if o['status'] == 'Cancelled'])
    }

    return render_template(
        'admin/reports.html',
        total_sales=total_sales,
        status_counts=status_counts,
        total_orders=len(all_orders)
    )

@admin_bp.route('/cities')
@role_required('admin')
def cities():
    """Manage operational multi-city delivery hubs."""
    return render_template('admin/cities.html', cities=CITIES)

@admin_bp.route('/diagnostics')
@role_required('admin')
def diagnostics():
    """System health diagnostics."""
    return render_template('admin/diagnostics.html')

@admin_bp.route('/audit-logs')
@role_required('admin')
def audit_logs():
    """Admin system audit logs."""
    logs = [
        {"id": 101, "event": "Order #1001 status changed to Delivered", "actor": "system", "time": "2026-08-28 13:15:00"},
        {"id": 102, "event": "Promo Coupon WELCOME50 applied by customer@foodflow.local", "actor": "customer", "time": "2026-08-28 12:31:00"},
        {"id": 103, "event": "User account restaurant@foodflow.local updated menu", "actor": "restaurant", "time": "2026-08-28 11:20:00"},
        {"id": 104, "event": "Admin user logged in from 127.0.0.1", "actor": "admin", "time": "2026-08-28 10:00:00"}
    ]
    return render_template('admin/audit_logs.html', logs=logs)
