"""Main Blueprint serving landing page, public discovery, and static pages."""
from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, flash
from data.categories import CATEGORIES
from data.restaurants import RESTAURANTS
from data.foods import FOODS
from data.offers import OFFERS
from data.cities import CITIES
from utils.filters import filter_restaurants, search_food_items
from utils.calculations import calculate_cart_totals

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Render home landing page with categories, featured restaurants, popular dishes, and promo offers."""
    selected_city = session.get('selected_city', 'Hyderabad')
    selected_area = session.get('selected_area', 'Jubilee Hills')

    featured_restaurants = [r for r in RESTAURANTS if r.get("is_featured")]
    popular_foods = [f for f in FOODS if f.get("is_best_seller")][:8]
    active_offers = [o for o in OFFERS if o.get("is_active")][:4]
    
    # Calculate stats for home counter
    stats = {
        "total_restaurants": len(RESTAURANTS),
        "total_dishes": len(FOODS),
        "happy_customers": "50,000+",
        "cities": len(CITIES)
    }
    
    return render_template(
        'customer/home.html',
        categories=CATEGORIES,
        featured_restaurants=featured_restaurants,
        popular_foods=popular_foods,
        active_offers=active_offers,
        stats=stats,
        cities=CITIES,
        selected_city=selected_city,
        selected_area=selected_area
    )

@main_bp.route('/location/select', methods=['POST'])
def select_location():
    """Update active delivery city and area in session."""
    city = request.form.get('city', 'Hyderabad').strip()
    area = request.form.get('area', 'Jubilee Hills').strip()

    session['selected_city'] = city
    session['selected_area'] = area
    session.modified = True

    flash(f"Delivery location updated to {area}, {city} 📍", "success")
    next_url = request.referrer or url_for('main.home')
    return redirect(next_url)

@main_bp.route('/about')
def about():
    """About FoodFlow project page."""
    return render_template('customer/about.html')

@main_bp.route('/contact')
def contact():
    """Contact & support page."""
    return render_template('customer/contact.html')

@main_bp.route('/search')
def search():
    """Search endpoint across restaurants and food items."""
    query = request.args.get('q', '').strip()
    
    matched_restaurants = filter_restaurants(query=query) if query else []
    matched_foods = search_food_items(query) if query else []
    
    return render_template(
        'customer/search.html',
        query=query,
        restaurants=matched_restaurants,
        foods=matched_foods,
        categories=CATEGORIES
    )
