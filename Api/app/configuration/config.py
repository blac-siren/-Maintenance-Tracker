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
        'DATABASE_URL', 'postgres://mqjunhtxyfszzn:c3c440040ffe1eb2e1f9aef28fe6dafac502035086e36b56ea5883501a33410b@ec2-54-83-59-120.compute-1.amazonaws.com:5432/de02p4etpinbrh')


class TestingConfig(Config):
    """Configuration for testing with a separate testing database."""

    TESTING = True
    DEBUG = False
    DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgresql://postgres:zakaria@localhost/trackertest')


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