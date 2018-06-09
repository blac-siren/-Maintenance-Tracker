"""Module handle functionality of database."""
from app.DB.conn import TrackerDB
import psycopg2

# instantiate class object
db = TrackerDB()


def insert_user(username, email, password, admin):
    """Insert user details into database."""
    try:

        db.cur.execute(
            "INSERT INTO users(username, email, password, admin) VALUES(%s,%s,%s,%s)",
            (username, email, password, admin))
        db.conn.commit()
    except (Exception, psycopg2.IntegrityError) as error:
        print(error)


def get_all_emails():
    """Get all emails."""
    db.query("SELECT email FROM users")
    existing_emails = db.cur.fetchall()
    return existing_emails


def get_password_hash(email):
    """Look for passwordhash in db."""
    db.cur.execute("""SELECT password FROM users WHERE email =%s""", (email, ))
    password_hash = db.cur.fetchone()
    return password_hash


def get_all_requests(email):
    """Get all request made by certain user."""
    db.cur.execute("""SELECT * FROM requests WHERE created_by = %s""",
                   (email, ))
    existing_requests = db.cur.fetchall()
    return existing_requests


def insert_request(user_request, category, location, status, created_by):
    """Insert request details in database."""
    try:
        db.cur.execute(
            "INSERT INTO requests(user_request, category, location, status, created_by) VALUES(%s,%s,%s,%s,%s)",
            (user_request, category, location, status, created_by))
        db.conn.commit()
    except (Exception, psycopg2.IntegrityError) as error:
        print(error)


def get_request(requestId):
    """Get a request id."""
    db.cur.execute("""SELECT * FROM requests WHERE id = %s""", (requestId, ))
    req = db.cur.fetchall()
    return req


def update_request(user_request, category, location, requestId):
    """Update existing request."""
    try:
        db.cur.execute(
            """UPDATE requests SET user_request=%s, category=%s, location=%s WHERE id=%s""",
            (user_request, category, location, requestId))
        db.conn.commit()
    except (Exception, psycopg2.IntegrityError) as error:
        print(error)


def delete_request(requestId):
    """Delete request by id."""
    db.cur.execute("""DELETE FROM requests WHERE id=%s""", (requestId, ))
    db.conn.commit()


def all_requests_admin():
    """Get all request for all users."""
    db.query("""SELECT * FROM requests""")
    all_req = db.cur.fetchall()
    return all_req


def update_status(status, requestId):
    """Admin approve/disapprove or reject request."""
    db.cur.execute("""UPDATE requests SET status=%s WHERE id=%s""",
                   (status, requestId))
    db.conn.commit()


def search_admin():
    """Search user admin in database."""
    db.cur.execute("""SELECT * FROM users WHERE admin=True""")
    all_admin = db.cur.fetchall()
    return all_admin


def confirm_admin(email):
    """Check if user is admin."""
    db.cur.execute("""SELECT * FROM users WHERE admin=True and email=%s""",
                   (email, ))
    variable = db.cur.fetchall()
    return variable
