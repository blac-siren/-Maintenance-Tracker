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
    DATABASE_URI = os.environ.get('DATABASE_URI', 'postgresql://postgres:zakaria@localhost/trackerapp')



class TestingConfig(Config):
    """Configuration for testing with a separate testing database."""

    TESTING = True
    DEBUG = True
    DATABASE_URI = os.environ.get('DATABASE_URI', 'postgresql://postgres:zakaria@localhost/trackertest')


class ProductionConfig(Config):
    """Config for production."""

    DEBUG = False
    TESTING = False
    DATABASE_URI = os.environ.get('DATABASE_URI', '')


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}