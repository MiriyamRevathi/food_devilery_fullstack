"""REST API Blueprint providing JSON endpoints for AJAX search, filter, recommendations, and exports."""
from flask import Blueprint, jsonify, request, Response, abort
from data.restaurants import RESTAURANTS
from data.foods import FOODS
from data.orders import get_all_orders, get_order_by_id
from utils.filters import filter_restaurants, search_food_items
from utils.recommendation_engine import get_recommended_foods_for_cart, get_similar_restaurants
from utils.pdf_generator import generate_order_invoice_html
from utils.export_helpers import export_orders_to_csv, export_menu_to_json

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/search/suggestions')
def search_suggestions():
    """Returns search autocomplete predictions."""
    q = request.args.get('q', '').strip().lower()
    if not q or len(q) < 2:
        return jsonify({'suggestions': []})

    matched_r = [r['name'] for r in RESTAURANTS if q in r['name'].lower()][:3]
    matched_f = [f['name'] for f in FOODS if q in f['name'].lower()][:5]

    return jsonify({
        'query': q,
        'suggestions': matched_r + matched_f
    })

@api_bp.route('/restaurants/filter')
def filter_restaurants_api():
    """API endpoint for dynamic restaurant filtering."""
    q = request.args.get('q', '').strip()
    cuisine = request.args.get('cuisine', '').strip()
    is_veg = request.args.get('veg', '') == '1'
    min_rating = float(request.args.get('min_rating', 0.0))
    sort_by = request.args.get('sort', 'rating').strip()

    results = filter_restaurants(
        query=q,
        cuisine=cuisine,
        is_veg=is_veg,
        min_rating=min_rating,
        sort_by=sort_by
    )

    return jsonify({
        'total': len(results),
        'restaurants': results[:20]
    })

@api_bp.route('/recommendations')
def get_recommendations_api():
    """API endpoint returning smart cart recommendations."""
    cart_items = [] # Can read from session
    recommendations = get_recommended_foods_for_cart(cart_items, FOODS)
    return jsonify({'recommendations': recommendations})

@api_bp.route('/orders/status/<order_id>')
def order_status_api(order_id):
    """API endpoint for live order status polling."""
    order = get_order_by_id(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    return jsonify({
        'order_number': order['order_number'],
        'status': order['status'],
        'history': order.get('status_history', [])
    })

@api_bp.route('/invoice/<order_id>')
def download_invoice_api(order_id):
    """Render HTML printable invoice."""
    order = get_order_by_id(order_id)
    if not order:
        abort(404)

    html_content = generate_order_invoice_html(order)
    return Response(html_content, mimetype='text/html')

@api_bp.route('/export/orders/csv')
def export_orders_csv_api():
    """Export orders to CSV download."""
    all_orders = get_all_orders()
    csv_data = export_orders_to_csv(all_orders)
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=foodflow_orders_report.csv'}
    )
