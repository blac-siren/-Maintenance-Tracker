"""Module for connection to database."""
import psycopg2
from app.configuration.config import app_config
from psycopg2.extras import RealDictCursor


class TrackerDB:
    """Class for database."""

    def init_app(self, config_name):
        """Database Constructor Method."""
        config_object = app_config[config_name]
        self.db = config_object.DATABASE_URI
        self.conn = psycopg2.connect(self.db, sslmode='require')
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def query(self, query):
        """Query execution method."""
        self.cur.execute(query)

    def close(self):
        """Close connection."""
        self.cur.close()
        self.conn.close()