"""Create table for the database."""
import psycopg2
from conn import TrackerDB

# instantiate class
db = TrackerDB()


def create_tables():
    """Create tables in postgres database."""

    db.query("""DROP TABLE IF EXISTS users""")
    db.query("""DROP TABLE IF EXISTS requests""")

    try:
        db.query("""
        CREATE TABLE users (id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL,
        admin VARCHAR(50) NOT NULL)""")

        db.query("""
        CREATE TABLE requests(id SERIAL PRIMARY KEY,
        user_request TEXT,
        category VARCHAR(50),
        location VARCHAR(100),
        status VARCHAR(100) NOT NULL,
        Created_by VARCHAR(100) NOT NULL,
        FOREIGN KEY (Created_by) REFERENCES users (email))""")

        db.conn.commit()
        db.conn.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)


# create_tables()


def default_admin():
    """Create a default Admin for the database."""
    try:
        db.query(
            "INSERT INTO users(username, email, password, admin) VALUES('Andela', 'andela@example.com', 'cohort28', True)",
        )
        db.conn.commit()
    except (Exception, psycopg2.IntegrityError) as error:
        print(error)


# default_admin()
