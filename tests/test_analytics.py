"""Unit tests for Statistical Analytics Engine."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.analytics_engine import (
    calculate_revenue_velocity,
    calculate_cuisine_popularity_matrix,
    calculate_driver_efficiency_scores,
    calculate_peak_order_hours
)
from data.orders import ORDERS
from data.foods import FOODS
from data.delivery import DELIVERY_PARTNERS

def test_revenue_velocity():
    velocity = calculate_revenue_velocity(ORDERS)
    assert 'total_revenue' in velocity
    assert 'total_orders' in velocity
    assert 'aov' in velocity
    assert velocity['total_orders'] >= 0

def test_cuisine_popularity_matrix():
    matrix = calculate_cuisine_popularity_matrix(ORDERS, FOODS)
    assert isinstance(matrix, dict)

def test_driver_efficiency_scores():
    scores = calculate_driver_efficiency_scores(ORDERS, DELIVERY_PARTNERS)
    assert len(scores) > 0
    assert 'efficiency_score' in scores[0]

def test_peak_order_hours():
    hours = calculate_peak_order_hours(ORDERS)
    assert len(hours) == 24
