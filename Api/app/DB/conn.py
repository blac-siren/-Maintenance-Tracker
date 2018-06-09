"""Module for connection to database."""
import psycopg2
from psycopg2.extras import RealDictCursor

conn_string = "dbname=trackerapp user=sirenblack password=cohort28 host=localhost"


class TrackerDB:
    """Class for database."""

    def __init__(self):
        """Database Constructor Method."""
        self.conn = psycopg2.connect(conn_string)
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def query(self, query):
        """Query execution method."""
        self.cur.execute(query)

    def close(self):
        """Close connection."""
        self.cur.close()
        self.conn.close()
