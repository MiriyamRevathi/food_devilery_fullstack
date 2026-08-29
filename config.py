import os

class Config:
    """Base configuration for FoodFlow Flask application."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'foodflow-super-secret-key-2026-offline-dev')
    APP_NAME = 'FoodFlow'
    TAGLINE = 'Delicious Food Delivered Fast to Your Doorstep'
    PER_PAGE = 12
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = True
    DEBUG = True
    
    # Currency Settings
    CURRENCY_SYMBOL = '₹'
    CURRENCY_CODE = 'INR'
    
    # Delivery & Tax rates
    DEFAULT_DELIVERY_FEE = 40.0
    FREE_DELIVERY_THRESHOLD = 500.0
    TAX_RATE_PERCENTAGE = 5.0
