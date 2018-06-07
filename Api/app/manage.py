"""Module for Database."""
import psycopg2
from psycopg2.extras import RealDictCursor
import json


def connectTODB():
    """Connect to database."""
    conn_string = "dbname=trackerapp user=sirenblack password=cohort28 host=localhost"
    print("Connecting to database>>>", conn_string)
    try:
        return psycopg2.connect(conn_string)
    except:
        print("Can't connect to database!")


def create_tables():
    """Create tables in postgres database."""
    commands = ("""
    CREATE TABLE users (id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL)
    """, """CREATE TABLE requests(id SERIAL PRIMARY KEY,
    user_request TEXT,
    category VARCHAR(50),
    location VARCHAR(100)),
    author INTEGER NOT NULL,
    FOREIGN KEY (author) REFERENCES users (id)""")
    # connect to PostgreSQL server
    try:
        conn = connectTODB()
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
            # close communication with postgreSQL database server.
            cur.close()
            # commit changes
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_user(username, email, password):
    """Insert user details into dictionary."""
    try:
        conn = connectTODB()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users(username, email, password) VALUES(%s,%s,%s)",
            (username, email, password))
        conn.commit()
        cur.execute("""SELECT * FROM users""")
        print(json.dumps(cur.fetchall(), indent=2))
        conn.close()
    except (Exception, psycopg2.IntegrityError) as error:
        print(error)


def all_email():
    """Check all email."""
    conn = connectTODB()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""SELECT email FROM users""")
    existing_emails = cur.fetchall()
    return existing_emails


def db_password_hash(email):
    """Look for password hash in db."""
    conn = connectTODB()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""SELECT password FROM users WHERE email =%s""", (email, ))
    password_hash = cur.fetchone()
    print(password_hash)
    return password_hash
