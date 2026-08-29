"""Order Service Layer for handling order creation, status workflows, and live tracking."""
from repositories.order_repository import order_repository
from data.orders import add_order, update_order_status
import datetime
import random

class OrderService:
    """Service class for order processing and tracking."""

    def place_order(self, user, cart, totals, delivery_address, phone, payment_method, special_instructions=''):
        """Process and record a new customer order."""
        if not cart:
            return None, "Cart is empty"

        restaurant_id = cart[0]['restaurant_id']
        new_id = len(order_repository.get_all()) + 1001
        order_num = f"ORD-2026-{random.randint(1000, 9999)}"
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_order = {
            "id": new_id,
            "order_number": order_num,
            "customer_id": user['id'],
            "customer_name": user['name'],
            "customer_phone": phone,
            "restaurant_id": restaurant_id,
            "restaurant_name": cart[0].get('restaurant_name', 'Paradise Biryani House'),
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
                {"status": "Order Placed", "time": datetime.datetime.now().strftime("%H:%M")}
            ]
        }

        add_order(new_order)
        return new_order, "Order placed successfully"

    def get_order_tracking(self, order_id):
        """Retrieve tracking status and stepper milestones for an order."""
        order = order_repository.get_by_id(order_id)
        if not order:
            return None, 0

        status_order_map = {
            "Order Placed": 0,
            "Confirmed": 1,
            "Preparing": 2,
            "Ready for Pickup": 3,
            "Out for Delivery": 4,
            "Delivered": 5,
            "Cancelled": -1
        }

        active_index = status_order_map.get(order.get('status'), 0)
        return order, active_index

order_service = OrderService()
