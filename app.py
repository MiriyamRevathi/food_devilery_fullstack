"""FoodFlow main application entrypoint."""
from flask import Flask, render_template, session
from config import Config
from routes.main import main_bp
from routes.auth import auth_bp
from routes.customer import customer_bp
from routes.restaurant import restaurant_bp
from routes.delivery import delivery_bp
from routes.admin import admin_bp
from routes.api import api_bp
from utils.helpers import format_currency, render_stars, time_ago
from utils.calculations import calculate_cart_totals
import datetime

def create_app():
    """Application factory for FoodFlow."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(delivery_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # Jinja Template Context Processor (global template variables)
    @app.context_processor
    def inject_globals():
        cart = session.get('cart', [])
        cart_totals = calculate_cart_totals(cart, coupon_code=session.get('applied_coupon'))
        current_user = session.get('user')
        
        return {
            'app_name': Config.APP_NAME,
            'tagline': Config.TAGLINE,
            'current_user': current_user,
            'cart': cart,
            'cart_count': cart_totals['item_count'],
            'cart_totals': cart_totals,
            'current_year': datetime.datetime.now().year,
            'currency_symbol': Config.CURRENCY_SYMBOL
        }

    # Register Jinja Filters
    @app.template_filter('currency')
    def currency_filter(val):
        return format_currency(val)

    @app.template_filter('stars')
    def stars_filter(val):
        return render_stars(val)

    @app.template_filter('time_ago')
    def time_ago_filter(val):
        return time_ago(val)

    # Global Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    return app

app = create_app()

if __name__ == '__main__':
    print(f"Starting {Config.APP_NAME} web server on http://127.0.0.1:5000 ...")
    app.run(host='127.0.0.1', port=5000, debug=True)
