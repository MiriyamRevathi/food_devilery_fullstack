"""Promo coupons dataset."""

OFFERS = [
    {
        "code": "WELCOME50",
        "discount_type": "percentage",
        "discount_value": 50.0,
        "min_order_amount": 199.0,
        "max_discount_amount": 100.0,
        "valid_until": "2026-12-31",
        "is_active": True,
        "description": "50% OFF up to \u20b9100 on your first order!",
        "badge": "New User"
    },
    {
        "code": "FOOD20",
        "discount_type": "percentage",
        "discount_value": 20.0,
        "min_order_amount": 299.0,
        "max_discount_amount": 120.0,
        "valid_until": "2026-12-31",
        "is_active": True,
        "description": "20% OFF up to \u20b9120 on all food orders over \u20b9299.",
        "badge": "Popular"
    },
    {
        "code": "SAVE100",
        "discount_type": "flat",
        "discount_value": 100.0,
        "min_order_amount": 499.0,
        "max_discount_amount": 100.0,
        "valid_until": "2026-12-31",
        "is_active": True,
        "description": "FLAT \u20b9100 OFF on mega cart orders above \u20b9499.",
        "badge": "Flat Discount"
    },
    {
        "code": "FIRSTORDER",
        "discount_type": "percentage",
        "discount_value": 60.0,
        "min_order_amount": 149.0,
        "max_discount_amount": 150.0,
        "valid_until": "2026-12-31",
        "is_active": True,
        "description": "Special 60% OFF up to \u20b9150 for brand new FoodFlow members.",
        "badge": "Exclusive"
    },
    {
        "code": "FREEDEL",
        "discount_type": "flat",
        "discount_value": 40.0,
        "min_order_amount": 200.0,
        "max_discount_amount": 40.0,
        "valid_until": "2026-12-31",
        "is_active": True,
        "description": "Free delivery waiver (\u20b940 OFF) on orders above \u20b9200.",
        "badge": "Free Delivery"
    },
    {
        "code": "PIZZA20",
        "discount_type": "percentage",
        "discount_value": 20.0,
        "min_order_amount": 400.0,
        "max_discount_amount": 150.0,
        "valid_until": "2026-12-31",
        "is_active": True,
        "description": "20% OFF on gourmet sourdough pizza orders.",
        "badge": "Category Special"
    },
    {
        "code": "STREET25",
        "discount_type": "percentage",
        "discount_value": 25.0,
        "min_order_amount": 150.0,
        "max_discount_amount": 60.0,
        "valid_until": "2026-12-31",
        "is_active": True,
        "description": "25% OFF up to \u20b960 on street food delicacies.",
        "badge": "Street Special"
    },
    {
        "code": "BIRYANI150",
        "discount_type": "flat",
        "discount_value": 150.0,
        "min_order_amount": 600.0,
        "max_discount_amount": 150.0,
        "valid_until": "2026-12-31",
        "is_active": True,
        "description": "FLAT \u20b9150 OFF on family biryani feast orders over \u20b9600.",
        "badge": "Feast Special"
    }
]
