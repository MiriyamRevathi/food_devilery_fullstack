"""Authentication Blueprint for FoodFlow handling login, register, logout, and profile."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from data.users import USERS
from utils.validators import validate_email, validate_phone, validate_password
from utils.decorators import login_required

auth_bp = Blueprint('auth', __name__)

def find_user_by_email(email):
    """Search user by email address (case-insensitive)."""
    if not email:
        return None
    e = email.strip().lower()
    for user in USERS:
        if user["email"].lower() == e:
            return user
    return None

def get_role_redirect_url(role):
    """Helper to return role-specific entrypoint URL."""
    if role == 'restaurant':
        return url_for('restaurant.dashboard')
    elif role == 'delivery':
        return url_for('delivery.dashboard')
    elif role == 'admin':
        return url_for('admin.dashboard')
    return url_for('main.home')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login endpoint supporting credentials and quick demo login."""
    if 'user' in session:
        return redirect(get_role_redirect_url(session['user']['role']))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            flash("Please enter both email and password.", "danger")
            return render_template('auth/login.html', email=email)

        user = find_user_by_email(email)
        if user and check_password_hash(user["password_hash"], password):
            # Store non-sensitive user info in session
            session['user'] = {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'role': user['role'],
                'phone': user.get('phone', ''),
                'address': user.get('address', ''),
                'avatar': user.get('avatar', ''),
                'restaurant_id': user.get('restaurant_id')
            }
            session.permanent = True
            flash(f"Welcome back, {user['name']}! Signed in as {user['role'].capitalize()}.", "success")

            return redirect(get_role_redirect_url(user['role']))

        flash("Invalid email or password. Please try again or use a demo account below.", "danger")
        return render_template('auth/login.html', email=email)

    return render_template('auth/login.html')

@auth_bp.route('/demo-login/<role>')
def demo_login(role):
    """Quick one-click login route for testing demo accounts."""
    role_email_map = {
        'customer': 'customer@foodflow.local',
        'restaurant': 'restaurant@foodflow.local',
        'delivery': 'delivery@foodflow.local',
        'admin': 'admin@foodflow.local'
    }

    email = role_email_map.get(role.lower())
    if not email:
        flash("Invalid demo role specified.", "danger")
        return redirect(url_for('auth.login'))

    user = find_user_by_email(email)
    if user:
        session['user'] = {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'role': user['role'],
            'phone': user.get('phone', ''),
            'address': user.get('address', ''),
            'avatar': user.get('avatar', ''),
            'restaurant_id': user.get('restaurant_id')
        }
        session.permanent = True
        flash(f"Quick Demo Login: Signed in as {user['name']} ({user['role'].capitalize()}).", "success")
        return redirect(get_role_redirect_url(user['role']))

    return redirect(url_for('main.home'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    if 'user' in session:
        return redirect(get_role_redirect_url(session['user']['role']))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '').strip()

        if not name or not validate_email(email) or not validate_password(password):
            flash("Please provide valid registration details.", "danger")
            return render_template('auth/register.html', name=name, email=email, phone=phone)

        if find_user_by_email(email):
            flash("An account with this email address already exists. Please sign in.", "warning")
            return render_template('auth/register.html', name=name, email=email, phone=phone)

        new_user = {
            "id": max(u['id'] for u in USERS) + 1,
            "name": name,
            "email": email,
            "password_hash": generate_password_hash(password),
            "role": "customer",
            "phone": phone,
            "avatar": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80"
        }
        USERS.append(new_user)
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    """Sign out user and clear session."""
    session.pop('user', None)
    session.pop('cart', None)
    session.pop('applied_coupon', None)
    flash("You have been signed out.", "info")
    return redirect(url_for('main.home'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile management."""
    current_user_id = session['user']['id']
    user = next((u for u in USERS if u['id'] == current_user_id), None)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()

        if name:
            user['name'] = name
            user['phone'] = phone
            user['address'] = address
            session['user']['name'] = name
            session['user']['phone'] = phone
            session['user']['address'] = address
            session.modified = True
            flash("Profile updated successfully!", "success")

    return render_template('customer/profile.html', user=user)

# Feature Auth: Session-based Authentication & Role Security Module
