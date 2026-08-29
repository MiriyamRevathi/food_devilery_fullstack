"""Integration tests for REST API endpoints."""
import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_api_suggestions(client):
    res = client.get('/api/v1/search/suggestions?q=Biryani')
    assert res.status_code == 200
    assert 'suggestions' in res.get_json()

def test_api_filter(client):
    res = client.get('/api/v1/restaurants/filter?cuisine=Biryani')
    assert res.status_code == 200
    assert 'restaurants' in res.get_json()

def test_api_invoice(client):
    res = client.get('/api/v1/invoice/1001')
    assert res.status_code == 200
    assert b'Invoice' in res.data

def test_api_export_csv(client):
    res = client.get('/api/v1/export/orders/csv')
    assert res.status_code == 200
    assert b'Order Number' in res.data
