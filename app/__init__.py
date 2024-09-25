from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Initialize SQLAlchemy, Migrate, and JWTManager instances
db = SQLAlchemy()  # SQLAlchemy object for database interaction
migrate = Migrate()  # Migrate object for handling database migrations
jwt = JWTManager()  # JWTManager object for handling JWT authentication

def create_app():
    """
    Factory function to create and configure the Flask application.
    This allows the application to be modular and reusable in different contexts.
    """
    app = Flask(__name__)  # Create the Flask app instance
    app.config.from_object('app.config.Config')  # Load configuration settings from config file

    # Initialize the app with SQLAlchemy, Flask-Migrate, and Flask-JWT-Extended
    db.init_app(app)  # Set up the database with the application
    migrate.init_app(app, db)  # Set up database migration utilities with the application and db
    jwt.init_app(app)  # Set up JWT handling with the application

    # Import and register the main blueprint for handling routes
    from .routes import main  # Import the blueprint from the routes module
    app.register_blueprint(main)  # Register the 'main' blueprint to handle routes

    return app  # Return the configured Flask application instance
