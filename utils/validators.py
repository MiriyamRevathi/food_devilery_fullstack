"""Input validation rules for forms and data."""
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
