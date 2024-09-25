import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///school.db')  # Use SQLite for local development
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')

