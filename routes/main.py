"""Main Blueprint serving public launch page, discovery, and static pages."""
from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, flash
from data.landing import EDITORIAL_CATEGORIES, DEMO_RESTAURANTS_PREVIEW, LAUNCH_STATS, FIRST_ORDER_OFFER, FOOD_STRIP_IMAGES
from data.categories import CATEGORIES
from data.restaurants import RESTAURANTS
from data.foods import FOODS
from data.offers import OFFERS
from data.cities import CITIES
from utils.filters import filter_restaurants, search_food_items

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Render Phase 1 public FoodFlow launch landing page."""
    selected_city = session.get('selected_city', 'Bengaluru')
    selected_area = session.get('selected_area', 'Indiranagar')

    return render_template(
        'customer/home.html',
        editorial_categories=EDITORIAL_CATEGORIES,
        preview_restaurants=DEMO_RESTAURANTS_PREVIEW,
        launch_stats=LAUNCH_STATS,
        first_order_offer=FIRST_ORDER_OFFER,
        food_strip_images=FOOD_STRIP_IMAGES,
        selected_city=selected_city,
        selected_area=selected_area,
        cities=CITIES
    )

@main_bp.route('/location/select', methods=['POST'])
def select_location():
    """Update active delivery city and area in session."""
    city = request.form.get('city', 'Bengaluru').strip()
    area = request.form.get('area', 'Indiranagar').strip()

    session['selected_city'] = city
    session['selected_area'] = area
    session.modified = True

    flash(f"Delivery location set to {area}, {city}", "success")
    next_url = request.referrer or url_for('main.home')
    return redirect(next_url)

@main_bp.route('/about')
def about():
    """About FoodFlow launch page."""
    return render_template('customer/about.html')

@main_bp.route('/contact')
def contact():
    """Contact & support page."""
    return render_template('customer/contact.html')

@main_bp.route('/search')
def search():
    """Public search endpoint across restaurants and dishes."""
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
