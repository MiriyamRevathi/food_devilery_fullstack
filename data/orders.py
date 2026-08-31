"""Order management data module."""
import datetime
from data.users import USERS
from utils.validators import validate_order_status_transition

ORDERS = [
    {
        "id": 1001,
        "order_number": "ORD-2026-8801",
        "customer_id": 1,
        "customer_name": "Demo Customer",
        "customer_email": "customer@foodflow.local",
        "customer_phone": "+91 98765 43210",
        "restaurant_id": 1,
        "restaurant_name": "Paradise Biryani House",
        "delivery_address": "Flat 402, Jubilee Hills, Hyderabad",
        "items": [
            {
                "food_id": 101,
                "name": "Special Dum Biryani",
                "price": 280.0,
                "quantity": 2,
                "variant": "Single Portion"
            }
        ],
        "subtotal": 560.0,
        "discount": 50.0,
        "delivery_fee": 40.0,
        "tax": 25.5,
        "total": 575.5,
        "payment_method": "Cash on Delivery",
        "payment_status": "Paid",
        "status": "Delivered",
        "delivery_agent_id": 3,
        "created_at": "2026-08-28 12:30:00",
        "status_history": [
            {"status": "Order Placed", "time": "12:30"},
            {"status": "Confirmed", "time": "12:32"},
            {"status": "Preparing", "time": "12:35"},
            {"status": "Ready for Pickup", "time": "12:50"},
            {"status": "Out for Delivery", "time": "12:55"},
            {"status": "Delivered", "time": "13:15"}
        ]
    }
]

def get_all_orders():
    """Retrieve list of all orders."""
    return ORDERS

def get_order_by_id(order_id):
    """Find order by ID or order number."""
    return next((o for o in ORDERS if str(o['id']) == str(order_id) or str(o.get('order_number')) == str(order_id)), None)

def add_order(order):
    """Add new order object to ORDERS list."""
    if 'status_history' not in order:
        time_short = datetime.datetime.now().strftime("%H:%M")
        order['status_history'] = [{"status": order.get('status', 'Order Placed'), "time": time_short}]
    ORDERS.insert(0, order)
    return order

def create_order(customer, cart_items, cart_totals, delivery_address, phone, payment_method):
    """Create and append new order to data store."""
    new_id = len(ORDERS) + 1001
    order_num = f"ORD-2026-{new_id}"
    
    restaurant_name = cart_items[0].get('restaurant_name', 'Paradise Biryani House') if cart_items else 'Paradise Biryani House'
    restaurant_id = cart_items[0].get('restaurant_id', 1) if cart_items else 1
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_short = datetime.datetime.now().strftime("%H:%M")

    new_order = {
        "id": new_id,
        "order_number": order_num,
        "customer_id": customer.get('id', 1),
        "customer_name": customer.get('name', 'Demo Customer'),
        "customer_email": customer.get('email', 'customer@foodflow.local'),
        "customer_phone": phone,
        "restaurant_id": restaurant_id,
        "restaurant_name": restaurant_name,
        "delivery_address": delivery_address,
        "items": cart_items,
        "subtotal": cart_totals['subtotal'],
        "discount": cart_totals['discount'],
        "delivery_fee": cart_totals['delivery_fee'],
        "tax": cart_totals['tax'],
        "total": cart_totals['total'],
        "payment_method": payment_method,
        "payment_status": "Paid" if payment_method != "Cash on Delivery" else "Pending COD",
        "status": "Order Placed",
        "delivery_agent_id": 3,
        "created_at": now_str,
        "status_history": [
            {"status": "Order Placed", "time": time_short}
        ]
    }
    
    add_order(new_order)
    return new_order

def update_order_status(order_id, new_status, is_admin=False):
    """Update order status with state machine transition validation."""
    order = get_order_by_id(order_id)
    if not order:
        return False, "Order not found."

    current_status = order.get('status', 'Order Placed')
    is_valid, msg = validate_order_status_transition(current_status, new_status, is_admin=is_admin)
    if not is_valid:
        return False, msg

    order['status'] = new_status
    if 'status_history' not in order:
        order['status_history'] = []
    
    time_short = datetime.datetime.now().strftime("%H:%M")
    if not any(h['status'] == new_status for h in order['status_history']):
        order['status_history'].append({"status": new_status, "time": time_short})

    return True, f"Order status updated to '{new_status}'."
