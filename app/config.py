import os  # Import the os module to interact with the operating system for environment variables

class Config:
    """
    Config class to hold configuration variables for the Flask application.
    Values are fetched from environment variables, with defaults provided.
    """

    # The secret key for securing sessions and sensitive operations within Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')  
    # Database URI to define the database connection. Uses environment variable DATABASE_URL if set, otherwise defaults to an SQLite database file.
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///school.db')  # Use SQLite for local development
    # Disables the SQLALCHEMY feature that tracks changes to objects, as it's not necessary and consumes extra memory.
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
    # Secret key specifically for JWT authentication, fetched from environment variable JWT_SECRET_KEY or uses a default value.
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
