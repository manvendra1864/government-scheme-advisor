from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, db
from models import User, SavedScheme
from utils import load_schemes, get_eligible_schemes, login_required
import logging

@app.route('/')
def index():
    """
    Main page - landing page
    """
    # Check if user is logged in and has complete profile
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    
    return render_template('index.html', user=user)

@app.route('/schemes')
@login_required
def schemes():
    """
    Schemes finder page
    """
    user = User.query.get(session['user_id'])
    
    if not user.has_complete_profile():
        return redirect(url_for('profile'))
    
    return render_template('schemes.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    User registration page
    """
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please login instead.', 'error')
            return render_template('register.html')
        
        # Create new user
        try:
            user = User(email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Registration error: {e}")
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login page
    """
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('login.html')
        
        # Find user and verify password
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            # Login successful
            session['user_id'] = user.id
            session['user_email'] = user.email
            flash(f'Welcome back!', 'success')
            
            # Redirect to profile if incomplete, otherwise to main page
            if not user.has_complete_profile():
                return redirect(url_for('profile'))
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """
    User logout
    """
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    User profile management page
    """
    user = User.query.get(session['user_id'])
    if user is None:
        flash("User not found. Please log in again.", "danger")
        return redirect(url_for('login'))  # or your login route name

    if request.method == 'POST':
        # Update user profile
        user.name = request.form.get('name', '').strip()
        user.age = request.form.get('age', type=int)
        user.gender = request.form.get('gender', '').lower()
        user.annual_income = request.form.get('annual_income', type=int)
        
        # Validation
        if not user.name or not user.age or not user.gender or user.annual_income is None:
            flash('All fields are required.', 'error')
            return render_template('profile.html', user=user)
        
        if user.age < 0 or user.age > 120:
            flash('Please enter a valid age.', 'error')
            return render_template('profile.html', user=user)
        
        if user.annual_income < 0:
            flash('Please enter a valid annual income.', 'error')
            return render_template('profile.html', user=user)
        
        if user.gender not in ['male', 'female', 'other']:
            flash('Please select a valid gender.', 'error')
            return render_template('profile.html', user=user)
        
        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Profile update error: {e}")
            flash('Failed to update profile. Please try again.', 'error')
    
    return render_template('profile.html', user=user)

@app.route('/check_eligibility', methods=['POST'])
@login_required
def check_eligibility():
    """
    API endpoint to check scheme eligibility based on user profile
    """
    user = User.query.get(session['user_id'])
    
    if not user.has_complete_profile():
        return jsonify({'error': 'Please complete your profile first.'}), 400
    
    # Load schemes and find eligible ones
    schemes = load_schemes()
    eligible_schemes = get_eligible_schemes(schemes, user.age, user.annual_income, user.gender)
    
    # Get list of saved scheme names for this user
    saved_scheme_names = [s.scheme_name for s in user.saved_schemes]
    
    # Add saved status to each scheme
    for scheme in eligible_schemes:
        scheme['is_saved'] = scheme['name'] in saved_scheme_names
    
    return jsonify({
        'schemes': eligible_schemes,
        'user_name': user.name,
        'count': len(eligible_schemes)
    })

@app.route('/save_scheme', methods=['POST'])
@login_required
def save_scheme():
    """
    API endpoint to save a scheme for the user
    """
    data = request.get_json()
    scheme_name = data.get('name')
    scheme_description = data.get('description')
    scheme_eligibility = data.get('eligibility')
    
    if not scheme_name:
        return jsonify({'error': 'Scheme name is required.'}), 400
    
    # Check if already saved
    existing = SavedScheme.query.filter_by(
        user_id=session['user_id'],
        scheme_name=scheme_name
    ).first()
    
    if existing:
        return jsonify({'error': 'Scheme already saved.'}), 400
    
    try:
        saved_scheme = SavedScheme(
            user_id=session['user_id'],
            scheme_name=scheme_name,
            scheme_description=scheme_description,
            scheme_eligibility=scheme_eligibility
        )
        db.session.add(saved_scheme)
        db.session.commit()
        
        return jsonify({'message': 'Scheme saved successfully!'})
    except Exception as e:
        db.session.rollback()
        logging.error(f"Save scheme error: {e}")
        return jsonify({'error': 'Failed to save scheme.'}), 500

@app.route('/remove_scheme', methods=['POST'])
@login_required
def remove_scheme():
    """
    API endpoint to remove a saved scheme
    """
    data = request.get_json()
    scheme_name = data.get('name')
    
    if not scheme_name:
        return jsonify({'error': 'Scheme name is required.'}), 400
    
    saved_scheme = SavedScheme.query.filter_by(
        user_id=session['user_id'],
        scheme_name=scheme_name
    ).first()
    
    if not saved_scheme:
        return jsonify({'error': 'Scheme not found in saved list.'}), 404
    
    try:
        db.session.delete(saved_scheme)
        db.session.commit()
        return jsonify({'message': 'Scheme removed successfully!'})
    except Exception as e:
        db.session.rollback()
        logging.error(f"Remove scheme error: {e}")
        return jsonify({'error': 'Failed to remove scheme.'}), 500

@app.route('/saved_schemes')
@login_required
def saved_schemes():
    """
    Page to display user's saved schemes
    """
    user = User.query.get(session['user_id'])
    saved_schemes_list = SavedScheme.query.filter_by(user_id=user.id).order_by(SavedScheme.saved_at.desc()).all()
    
    return render_template('saved_schemes.html', user=user, saved_schemes=saved_schemes_list)

@app.route("/")
def home():
    return render_template("index.html")  # Make sure you have templates/index.html
