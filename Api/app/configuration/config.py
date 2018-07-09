"""App configuration."""
import os


class Config:
    """Parent configuration file."""

    DEBUG = False
    SECRET = os.getenv('SECRET')


class DevelopmentConfig(Config):
    """Configuration for development."""

    DEBUG = False
    TESTING = False
    DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgresql://postgres:zakaria@localhost:5432/trackerapp')


class TestingConfig(Config):
    """Configuration for testing with a separate testing database."""

    TESTING = True
    DEBUG = False
    DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgresql://postgres:zakaria@localhost:5432/trackertest')


class ProductionConfig(Config):
    """Config for production."""

    DEBUG = False
    TESTING = False
    DATABASE_URI = os.environ.get('DATABASE_URL', '')


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}