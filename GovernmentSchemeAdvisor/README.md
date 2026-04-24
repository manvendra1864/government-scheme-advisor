# My Yojana - Government Welfare Scheme Finder

## Overview

My Yojana is a Flask-based web application that helps users discover government welfare schemes they're eligible for based on their personal information. The application features user authentication, profile management, and personalized scheme recommendations using a JSON-based eligibility system.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask
- **Styling**: Custom CSS with Poppins font family and purple theme
- **JavaScript**: Vanilla JavaScript for dynamic interactions
- **UI Framework**: Bootstrap 5.1.3 for enhanced form styling
- **Responsive Design**: Mobile-first approach with viewport meta tags

### Backend Architecture
- **Framework**: Flask (Python 3.11)
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Database**: SQLite (development) with PostgreSQL support configured
- **Session Management**: Flask sessions with server-side storage
- **Password Security**: Werkzeug password hashing

### Template Structure
- Base template (`base.html`) with navigation and flash messaging
- Authentication templates (`login.html`, `register.html`)
- User interface templates (`index.html`, `profile.html`, `saved_schemes.html`)

## Key Components

### Authentication System
- User registration with email validation
- Password hashing using Werkzeug
- Session-based authentication
- Login required decorators for protected routes

### User Profile Management
- Complete profile tracking (name, age, gender, annual income)
- Profile completion validation
- Profile editing capabilities

### Scheme Eligibility Engine
- JSON-based scheme database (`static/schemes.json`)
- Multi-criteria filtering (age, income, gender)
- Real-time eligibility checking
- Scheme saving functionality

### Database Models
- **User Model**: Authentication and profile data with timestamps
- **SavedScheme Model**: User's saved schemes with metadata
- Relationship mapping between users and saved schemes

## Data Flow

1. **User Registration/Login**: 
   - User creates account or logs in
   - Session established with user ID

2. **Profile Completion**:
   - User fills profile information
   - System validates completeness before scheme access

3. **Scheme Discovery**:
   - System loads schemes from JSON file
   - Filters based on user's age, income, and gender
   - Returns eligible schemes via AJAX

4. **Scheme Management**:
   - Users can save interesting schemes
   - Saved schemes stored in database with timestamps
   - Users can view and manage saved schemes

## External Dependencies

### Python Packages
- **Flask**: Web framework and routing
- **Flask-SQLAlchemy**: Database ORM integration
- **email-validator**: Email validation with DNS checking
- **psycopg2-binary**: PostgreSQL adapter (production ready)
- **gunicorn**: WSGI HTTP server for deployment
- **werkzeug**: WSGI utilities and password hashing

### Frontend Dependencies
- **Bootstrap 5.1.3**: CSS framework (CDN)
- **Google Fonts**: Poppins font family (CDN)

### System Dependencies
- **PostgreSQL**: Database server (configured in Nix)
- **OpenSSL**: Security libraries

## Deployment Strategy

### Development Environment
- **Platform**: Replit with Nix package management
- **Database**: SQLite for simplicity
- **Server**: Flask development server with debug mode
- **Port**: 5000 with host binding to 0.0.0.0

### Production Configuration
- **Deployment Target**: Autoscale deployment on Replit
- **WSGI Server**: Gunicorn with process binding
- **Database**: PostgreSQL (environment variable configurable)
- **Security**: Environment-based secret key management
- **Proxy Support**: ProxyFix middleware for proper URL generation

### Environment Variables
- `DATABASE_URL`: Database connection string
- `SESSION_SECRET`: Flask session secret key

## Changelog
- June 24, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.