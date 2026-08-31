"""Input validation rules for forms, data, and state machine transitions."""
import re

def validate_email(email):
    """Check if email address is valid."""
    if not email or not isinstance(email, str):
        return False
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email.strip()) is not None

def validate_phone(phone):
    """Check if phone number is valid 10-digit Indian number."""
    if not phone or not isinstance(phone, str):
        return False
    digits = re.sub(r'\D', '', phone)
    return len(digits) >= 10

def validate_password(password):
    """Validate password strength (min 6 chars)."""
    return bool(password and len(password) >= 6)

# Valid Order Status State Machine Transitions
VALID_ORDER_TRANSITIONS = {
    'Order Placed': ['Confirmed', 'Cancelled'],
    'Confirmed': ['Preparing', 'Cancelled'],
    'Preparing': ['Ready for Pickup'],
    'Ready for Pickup': ['Out for Delivery'],
    'Out for Delivery': ['Delivered'],
    'Delivered': [],
    'Cancelled': []
}

def validate_order_status_transition(current_status, new_status, is_admin=False):
    """
    Validate state machine transition for order status.
    Returns (is_valid, error_message).
    """
    if not current_status or not new_status:
        return False, "Invalid status values provided."

    if current_status == new_status:
        return True, ""

    if current_status in ['Delivered', 'Cancelled'] and not is_admin:
        return False, f"Order is already in terminal state '{current_status}' and cannot be modified."

    allowed = VALID_ORDER_TRANSITIONS.get(current_status, [])
    if new_status in allowed or is_admin:
        return True, ""

    return False, f"Cannot transition order status from '{current_status}' to '{new_status}'."
