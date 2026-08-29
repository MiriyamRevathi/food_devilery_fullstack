"""Unit tests for Geo Distance and ETA calculation."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.geo_helpers import calculate_haversine_distance, estimate_delivery_eta_and_fee

def test_haversine_distance():
    # Hyderabad to Bengaluru approximate distance (~500 km)
    dist = calculate_haversine_distance(17.385044, 78.486671, 12.971599, 77.594566)
    assert dist > 450.0

def test_eta_and_fee_estimation():
    result = estimate_delivery_eta_and_fee(17.385044, 78.486671, 17.400000, 78.500000)
    assert 'distance_km' in result
    assert 'estimated_mins' in result
    assert 'delivery_fee' in result
    assert result['delivery_fee'] >= 30.0
