"""Automated Pytest test suite for FoodFlow application."""
import sys
import os
import pytest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from data.orders import ORDERS, update_order_status
from data.users import USERS
from utils.validators import validate_order_status_transition

@pytest.fixture
def client():
    """Create Flask test client for pytest."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test landing page renders status 200 and key components."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'FoodFlow' in response.data
    assert b'Biryani' in response.data

def test_restaurant_listing_and_filter(client):
    """Test restaurant directory and cuisine filtering."""
    res1 = client.get('/restaurants')
    assert res1.status_code == 200

    res2 = client.get('/restaurants?cuisine=Biryani&min_rating=4.5&veg=1')
    assert res2.status_code == 200

def test_restaurant_detail_page(client):
    """Test restaurant detail menu page."""
    response = client.get('/restaurant/paradise-biryani-house-1')
    assert response.status_code == 200

def test_authentication_flow(client):
    """Test login and demo login routes."""
    assert client.get('/login').status_code == 200

    res_bad = client.post('/login', data={'email': 'wrong@foodflow.local', 'password': 'bad'})
    assert b'Invalid email or password' in res_bad.data

    res_demo = client.get('/demo-login/customer', follow_redirects=True)
    assert res_demo.status_code == 200
    assert b'Demo Customer' in res_demo.data

def test_role_protection(client):
    """Test role-based access control decorators."""
    res = client.get('/admin/dashboard')
    assert res.status_code in [302, 403]

    client.get('/demo-login/customer')
    res_forbidden = client.get('/admin/dashboard')
    assert res_forbidden.status_code == 403

def test_cart_operations(client):
    """Test cart add, update, coupon application, and financial calculations."""
    res_add = client.post('/api/cart/add', json={'food_id': 101, 'quantity': 2, 'variant': 'Single Portion'})
    assert res_add.status_code == 200
    assert res_add.get_json()['success'] is True

    res_cart = client.get('/cart')
    assert res_cart.status_code == 200
    assert b'Dum Biryani' in res_cart.data

    res_coupon = client.post('/api/cart/coupon', json={'code': 'WELCOME50', 'action': 'apply'})
    assert res_coupon.status_code == 200
    assert res_coupon.get_json()['totals']['discount'] == 100.0

def test_checkout_and_order_creation(client):
    """Test full checkout flow and order creation."""
    client.get('/demo-login/customer')
    client.post('/api/cart/add', json={'food_id': 101, 'quantity': 1})

    initial_orders_count = len(ORDERS)

    res_checkout = client.post('/checkout', data={
        'phone': '+91 98765 43210',
        'address': 'Flat 101, Pytest Street, Bengaluru',
        'payment_method': 'Cash on Delivery'
    }, follow_redirects=True)

    assert res_checkout.status_code == 200
    assert len(ORDERS) == initial_orders_count + 1
    assert b'Order Confirmed!' in res_checkout.data

def test_order_state_machine_transitions():
    """Test order status state machine rules."""
    valid, msg = validate_order_status_transition('Order Placed', 'Confirmed')
    assert valid is True

    valid_invalid, msg_invalid = validate_order_status_transition('Delivered', 'Preparing')
    assert valid_invalid is False
    assert 'terminal state' in msg_invalid or 'Cannot transition' in msg_invalid

def test_favorites_and_addresses(client):
    """Test favorites wishlist and delivery address management."""
    client.get('/demo-login/customer')

    res_fav = client.get('/favorites')
    assert res_fav.status_code == 200

    res_addr = client.get('/addresses')
    assert res_addr.status_code == 200

    res_add_addr = client.post('/addresses/add', data={
        'label': 'WORK',
        'name': 'Demo Customer',
        'address': 'Cyber Towers, HITECH City',
        'city': 'Hyderabad',
        'phone': '+91 98765 43210'
    }, follow_redirects=True)
    assert res_add_addr.status_code == 200
    assert b'Cyber Towers' in res_add_addr.data

def test_restaurant_inventory_and_menu(client):
    """Test restaurant partner inventory and menu management."""
    client.get('/demo-login/restaurant')

    res_inv = client.get('/restaurant/inventory')
    assert res_inv.status_code == 200

    res_restock = client.post('/restaurant/inventory/restock/1', data={'quantity': 50}, follow_redirects=True)
    assert res_restock.status_code == 200

def test_delivery_driver_workflow(client):
    """Test delivery partner dashboard and active delivery stepper."""
    client.get('/demo-login/delivery')

    res_dash = client.get('/delivery/dashboard')
    assert res_dash.status_code == 200

    res_act = client.get('/delivery/active')
    assert res_act.status_code == 200

def test_admin_management_controls(client):
    """Test admin portal user and promo coupon controls."""
    client.get('/demo-login/admin')

    res_users = client.get('/admin/users')
    assert res_users.status_code == 200

    res_offers = client.get('/admin/offers')
    assert res_offers.status_code == 200

def test_custom_error_pages(client):
    """Test custom 404 page for non-existent routes."""
    res_404 = client.get('/this-route-does-not-exist')
    assert res_404.status_code == 404
    assert b'Looks like this page got eaten!' in res_404.data
