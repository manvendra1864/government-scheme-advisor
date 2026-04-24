import json
import os
from functools import wraps
from flask import session, redirect, url_for, flash

def load_schemes():
    """
    Load government schemes from JSON file
    """
    try:
        schemes_path = os.path.join('static', 'schemes.json')
        with open(schemes_path, 'r', encoding='utf-8') as file:
            schemes = json.load(file)
        return schemes
    except FileNotFoundError:
        print("Error: schemes.json file not found")
        return []
    except json.JSONDecodeError:
        print("Error: Invalid JSON in schemes.json")
        return []

def get_eligible_schemes(schemes, age, income, gender):
    """
    Filter schemes based on user eligibility criteria
    
    Args:
        schemes (list): List of scheme dictionaries
        age (int): User's age
        income (int): User's annual income
        gender (str): User's gender ('male', 'female', 'other')
    
    Returns:
        list: List of eligible schemes
    """
    eligible = []
    
    for scheme in schemes:
        # Check age eligibility
        if age < scheme.get('age', {}).get('min', 0) or age > scheme.get('age', {}).get('max', 100):
            continue
        
        # Check income eligibility
        if income > scheme.get('maxIncome', float('inf')):
            continue
        
        # Check gender eligibility
        scheme_gender = scheme.get('gender', 'any')
        if scheme_gender != 'any' and scheme_gender != gender:
            continue
        
        # Scheme is eligible
        eligible.append(scheme)
    
    return eligible

def login_required(f):
    """
    Decorator to require user login for certain routes
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        
        # Verify user still exists in database
        from models import User
        user = User.query.get(session['user_id'])
        if user is None:
            session.clear()
            flash('Your session has expired. Please log in again.', 'error')
            return redirect(url_for('login'))
            
        return f(*args, **kwargs)
    return decorated_function
