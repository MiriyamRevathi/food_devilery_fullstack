"""Cart total, discounts, delivery fee, and tax calculations."""
from config import Config
from data.offers import OFFERS

def calculate_cart_totals(cart_items, coupon_code=None):
    """
    Calculate cart financial summary:
    - subtotal
    - discount amount (via applied coupon)
    - delivery fee (free above threshold)
    - taxes (5% GST)
    - final payable total
    """
    subtotal = 0.0
    for item in cart_items:
        item_price = float(item.get("price", 0.0))
        variant_price = float(item.get("variant_price", 0.0))
        
        # Robust add-ons calculation (handles dicts and strings)
        add_ons_price = 0.0
        for addon in item.get("add_ons", []):
            if isinstance(addon, dict):
                add_ons_price += float(addon.get("price", 0.0))
                
        quantity = int(item.get("quantity", 1))
        
        unit_price = item_price + variant_price + add_ons_price
        subtotal += unit_price * quantity
    
    # Calculate discount from coupon
    discount_amount = 0.0
    applied_coupon = None
    
    if coupon_code and subtotal > 0:
        for offer in OFFERS:
            if offer["code"].upper() == coupon_code.upper() and offer["is_active"]:
                if subtotal >= offer["min_order_amount"]:
                    if offer["discount_type"] == "percentage":
                        raw_discount = (subtotal * offer["discount_value"]) / 100.0
                        discount_amount = min(raw_discount, offer["max_discount_amount"])
                    elif offer["discount_type"] == "flat":
                        discount_amount = offer["discount_value"]
                    applied_coupon = offer
                break
    
    discounted_subtotal = max(0.0, subtotal - discount_amount)
    
    # Delivery fee logic
    if subtotal >= Config.FREE_DELIVERY_THRESHOLD or subtotal == 0:
        delivery_fee = 0.0
    else:
        delivery_fee = Config.DEFAULT_DELIVERY_FEE
        
    # Tax calculation (5% on discounted subtotal)
    tax_amount = round((discounted_subtotal * Config.TAX_RATE_PERCENTAGE) / 100.0, 2)
    
    final_total = round(discounted_subtotal + delivery_fee + tax_amount, 2)
    
    return {
        "subtotal": round(subtotal, 2),
        "discount": round(discount_amount, 2),
        "coupon_code": coupon_code.upper() if applied_coupon else None,
        "applied_coupon": applied_coupon,
        "delivery_fee": round(delivery_fee, 2),
        "tax": tax_amount,
        "final_total": final_total,
        "item_count": sum(int(item.get("quantity", 1)) for item in cart_items)
    }
