"""Create table for the database."""
import psycopg2
from app.DB.conn import TrackerDB


def create_tables(db):
    """Create tables in postgres database."""

    db.query("""DROP TABLE IF EXISTS users CASCADE""")
    db.query("""DROP TABLE IF EXISTS requests CASCADE""")

    try:
        db.query("""
        CREATE TABLE users (id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL,
        admin BOOLEAN NOT NULL)""")

        db.query("""
        CREATE TABLE requests(id SERIAL PRIMARY KEY,
        user_request TEXT,
        category VARCHAR(50),
        location VARCHAR(100),
        status VARCHAR(100) NOT NULL,
        Created_by VARCHAR(100) NOT NULL,
        FOREIGN KEY (Created_by) REFERENCES users (email))""")

        db.conn.commit()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
        db.conn.rollback()


def run_migrations(migration):
    db = TrackerDB()
    db.init_app(migration)
    create_tables(db)


