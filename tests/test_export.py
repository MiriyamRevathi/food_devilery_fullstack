"""Unit tests for Export Helpers module."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.export_helpers import export_orders_to_csv, export_menu_to_json
from data.orders import ORDERS
from data.foods import FOODS

def test_export_orders_csv():
    csv_str = export_orders_to_csv(ORDERS)
    assert 'Order Number' in csv_str
    assert 'ORD-2026' in csv_str

def test_export_menu_json():
    json_str = export_menu_to_json(FOODS[:10])
    assert 'id' in json_str
