"""Role-based protection decorators for Flask routes."""
from functools import wraps
from flask import session, redirect, url_for, flash, render_template

def login_required(f):
    """Ensure user is logged in before accessing route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """Ensure logged in user has one of required roles."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                flash("Please sign in first.", "warning")
                return redirect(url_for('auth.login'))
            user_role = session['user'].get('role')
            if user_role not in roles:
                return render_template('errors/403.html'), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
