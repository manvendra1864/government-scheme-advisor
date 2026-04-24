import os
import logging
from flask import Flask
from extensions import db
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create Flask application instance
app = Flask(__name__)

# Configure secret key for sessions (required for Flask sessions)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Configure proxy fix for proper URL generation
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure SQLite database
db_url = os.environ.get("DATABASE_URL", "sqlite:///yojana.db")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the database with the app
db.init_app(app)

# Import routes after app initialization but before table creation
from routes import *  # noqa: F401

# Create tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    # Run the application on port 5000 for development
    app.run(host="0.0.0.0", port=5000, debug=True)