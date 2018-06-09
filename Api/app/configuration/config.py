"""App configuration."""
import os


class Config:
    """parent configuration file."""

    DEBUG = False
    SECRET = os.getenv('SECRET')


class DevelopmentConfig(Config):
    """configuration for development."""

    DEBUG = True
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
}