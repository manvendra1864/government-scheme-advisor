from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """
    User model for storing user authentication and profile information
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    
    # Profile information
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)  # 'male', 'female', 'other'
    annual_income = db.Column(db.Integer, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to saved schemes
    saved_schemes = db.relationship('SavedScheme', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the stored hash"""
        return check_password_hash(self.password_hash, password)
    
    def has_complete_profile(self):
        """Check if user has completed their profile"""
        return all([self.name, self.age, self.gender, self.annual_income is not None])
    
    def __repr__(self):
        return f'<User {self.email}>'

class SavedScheme(db.Model):
    """
    Model for storing user's saved government schemes
    """
    __tablename__ = 'saved_schemes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    scheme_name = db.Column(db.String(200), nullable=False)
    scheme_description = db.Column(db.Text, nullable=True)
    scheme_eligibility = db.Column(db.Text, nullable=True)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint to prevent duplicate saves
    __table_args__ = (db.UniqueConstraint('user_id', 'scheme_name', name='unique_user_scheme'),)
    
    def __repr__(self):
        return f'<SavedScheme {self.scheme_name} for User {self.user_id}>'
