# My Yojana – Government Welfare Scheme Advisor

A smart web application that helps citizens discover government welfare schemes based on their personal profile and eligibility criteria.

🌐 **Live Demo:** https://government-scheme-advisor-1.onrender.com/

---

## Overview

**My Yojana** is a Flask-powered web platform designed to simplify access to government welfare schemes. Users can create an account, complete their profile, and instantly receive personalized scheme recommendations based on factors such as age, gender, and annual income.

The platform aims to bridge the information gap between citizens and government welfare programs by providing an intuitive, user-friendly, and accessible experience.

---

## Features

### User Authentication

* Secure user registration and login
* Password hashing using Werkzeug
* Session-based authentication
* Protected routes for authorized users

### Profile Management

* Personal profile creation and updates
* Stores demographic and financial information
* Profile completion validation before recommendations

### Personalized Scheme Recommendations

* Eligibility-based scheme matching
* Real-time filtering using user profile data
* Multi-criteria evaluation including:

  * Age
  * Gender
  * Annual Income

### Saved Schemes

* Save schemes for future reference
* View and manage bookmarked schemes
* Persistent storage using a relational database

---

## Technology Stack

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* Jinja2 Templates
* Vanilla JavaScript

### Backend

* Python 3.11
* Flask
* Flask-SQLAlchemy
* Werkzeug Security

### Database

* SQLite (Development)
* PostgreSQL (Production Ready)

### Deployment

* Gunicorn
* Render
* Environment-based configuration

---

## System Architecture

### Application Flow

1. User registers or logs into the platform.
2. User completes their profile information.
3. The eligibility engine evaluates available schemes.
4. Matching schemes are displayed to the user.
5. Users can save schemes for later access.

### Eligibility Engine

The recommendation system uses a JSON-based scheme repository and evaluates:

* Minimum and maximum age requirements
* Income eligibility criteria
* Gender-specific requirements

Only schemes matching the user's profile are displayed.

---

## Database Models

### User

Stores:

* Authentication credentials
* Personal information
* Profile completion status
* Account timestamps

### SavedScheme

Stores:

* Saved scheme information
* User associations
* Creation timestamps

---

## Project Structure

```text
├── app.py
├── models.py
├── routes.py
├── static/
│   ├── styles.css
│   └── schemes.json
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── index.html
│   └── saved_schemes.html
└── requirements.txt
```

---

## Installation

### Clone the Repository

```bash
git clone <repository-url>
cd my-yojana
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

```env
DATABASE_URL=your_database_url
SESSION_SECRET=your_secret_key
```

### Run the Application

```bash
python app.py
```

Application will be available at:

```text
http://localhost:5000
```

---

## Future Enhancements

* AI-powered scheme recommendations
* Multilingual support
* Aadhaar-based verification
* Scheme application tracking
* Government API integrations
* Mobile application support

---

## Security Features

* Password hashing and secure authentication
* Session protection
* Environment-based secret management
* Production-ready PostgreSQL support

---

## Live Application

🔗 https://government-scheme-advisor-1.onrender.com/

---

## License

This project is developed for educational and social impact purposes. Feel free to modify and extend it according to your requirements.

---

## Author

**Manvendra Singh**

Computer Science Student | Python & Flask Developer

LinkedIn: https://linkedin.com/in/manvendra1864
