"""Order Repository Layer for managing customer order records and status updates."""

class OrderRepository:
    """Repository class for order management."""

    def __init__(self):
        self._orders = [
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
        "created_at": "2026-08-28 12:30:00"
    }
]

    def get_all(self):
        """Retrieve all order records."""
        return self._orders

    def get_by_id(self, order_id):
        """Find order by ID or order number."""
        return next((o for o in self._orders if str(o['id']) == str(order_id) or str(o.get('order_number')) == str(order_id)), None)

    def get_by_customer(self, customer_id):
        """Retrieve all orders placed by a specific customer."""
        return [o for o in self._orders if str(o.get('customer_id')) == str(customer_id)]

    def get_by_restaurant(self, restaurant_id):
        """Retrieve orders received by a specific restaurant."""
        return [o for o in self._orders if str(o.get('restaurant_id')) == str(restaurant_id)]

    def get_by_driver(self, driver_id):
        """Retrieve orders assigned to a delivery driver."""
        return [o for o in self._orders if str(o.get('delivery_agent_id')) == str(driver_id)]

order_repository = OrderRepository()
