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

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login endpoint supporting credentials and quick demo login."""
    if 'user' in session:
        return redirect(url_for('main.home'))

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

            # Redirect based on role
            role = user['role']
            if role == 'restaurant':
                return redirect(url_for('main.home')) # Will point to restaurant dashboard in Phase 6
            elif role == 'delivery':
                return redirect(url_for('main.home')) # Will point to delivery dashboard in Phase 7
            elif role == 'admin':
                return redirect(url_for('main.home')) # Will point to admin dashboard in Phase 8
            else:
                return redirect(url_for('main.home'))

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

    return redirect(url_for('main.home'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    if 'user' in session:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        address = request.form.get('address', '').strip()
        role = request.form.get('role', 'customer').strip()

        # Validation
        if not name or not email or not password:
            flash("Name, email, and password are required.", "danger")
            return render_template('auth/register.html')

        if not validate_email(email):
            flash("Please enter a valid email address.", "danger")
            return render_template('auth/register.html')

        if find_user_by_email(email):
            flash("An account with this email already exists. Please log in.", "warning")
            return redirect(url_for('auth.login'))

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template('auth/register.html')

        if not validate_password(password):
            flash("Password must be at least 6 characters long.", "danger")
            return render_template('auth/register.html')

        # Create new user record
        new_id = len(USERS) + 1
        new_user = {
            'id': new_id,
            'name': name,
            'email': email,
            'password_hash': generate_password_hash(password),
            'role': role if role in ['customer', 'restaurant', 'delivery'] else 'customer',
            'phone': phone,
            'address': address,
            'avatar': "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80"
        }

        USERS.append(new_user)

        # Log in newly registered user
        session['user'] = {
            'id': new_user['id'],
            'name': new_user['name'],
            'email': new_user['email'],
            'role': new_user['role'],
            'phone': new_user['phone'],
            'address': new_user['address'],
            'avatar': new_user['avatar']
        }
        session.permanent = True

        flash(f"Account created successfully! Welcome to FoodFlow, {name}.", "success")
        return redirect(url_for('main.home'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    """User sign out route."""
    user_name = session.get('user', {}).get('name', 'User')
    session.pop('user', None)
    flash(f"Goodbye {user_name}, you have signed out successfully.", "info")
    return redirect(url_for('main.home'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Customer profile view and edit page."""
    current_user_id = session['user']['id']
    user = next((u for u in USERS if u['id'] == current_user_id), None)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()

        if name:
            if user:
                user['name'] = name
                user['phone'] = phone
                user['address'] = address

            # Update session state
            session['user']['name'] = name
            session['user']['phone'] = phone
            session['user']['address'] = address
            session.modified = True

            flash("Your profile details have been updated!", "success")
            return redirect(url_for('auth.profile'))

    return render_template('customer/profile.html', user=user or session['user'])

# Feature Auth: Session-based Authentication & Role Security Module

# Feature Auth: Session-based Authentication & Role Security Module
