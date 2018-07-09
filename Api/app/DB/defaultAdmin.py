"""Default admin."""
import psycopg2
from app.DB.conn import TrackerDB
from flask_bcrypt import Bcrypt


def userAdmin(db):
    password = Bcrypt().generate_password_hash("Password123").decode('UTF-8')
    try:
        db.cur.execute(
            "INSERT INTO users(username, email, password, admin) VALUES(%s,%s,%s,%s)",
            ("Admin", "admin@admin.com", password, True))
        db.conn.commit()
    except (Exception, psycopg2.IntegrityError) as error:
        print(error)


def create_admin(migration):
    db = TrackerDB()
    db.init_app(migration)
    userAdmin(db)
