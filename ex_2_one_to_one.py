"""
The reason why you'll want to use a 1-to-1 relationship is generally
when you are extending the idea of something.
So, instead of having one table that represents one idea, you can extend it.
"""

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


DB_FILE = os.path.splitext(__file__)[0] + ".db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_FILE}"
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    # to make the following into a 1-to-1 relationship,
    # the only thing we have to do is add `uselist=False`
    # (you can think of `uselist` as a "list of children")
    profile = db.relationship("Profile", backref="owner", uselist=False)


class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    # If you go into your DB and modified it directly,
    # you will be able to create multiple Profile records with the same user_id.
    # But Flask-SQLAlchemy isn't going to do that.
    # If you do think you'll go through the DB,
    # adding `unique=True` to the following will make things safer.
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)


if __name__ == "__main__":
    if os.path.exists(DB_FILE):
        print()
        print(f"found {os.path.abspath(DB_FILE)} - removing and re-creating it...")
        os.remove(DB_FILE)

    db.create_all()

    user = User(name="John Doe")
    profile_v1 = Profile(name="John Doe's Profile v1", owner=user)
    db.session.add(user)
    db.session.add(profile_v1)
    db.session.commit()

    profile_v2 = Profile(name="John Doe's Profile v2", owner=user)
    db.session.add(profile_v2)
    db.session.commit()
