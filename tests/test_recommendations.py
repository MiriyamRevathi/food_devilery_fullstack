"""Unit tests for Smart Recommendation Engine."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.recommendation_engine import (
    get_recommended_foods_for_cart,
    get_similar_restaurants
)
from data.foods import FOODS
from data.restaurants import RESTAURANTS

def test_empty_cart_recommendations():
    recs = get_recommended_foods_for_cart([], FOODS)
    assert len(recs) <= 6

def test_similar_restaurants():
    r = RESTAURANTS[0]
    similar = get_similar_restaurants(r, RESTAURANTS)
    assert isinstance(similar, list)
