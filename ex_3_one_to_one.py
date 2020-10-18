import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


DB_FILE = "ex_3_one_to_one.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_FILE}"
db = SQLAlchemy(app)


class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    # to make the following into a 1-to-1 relationship,
    # the only thing we have to do is add `uselist=False`
    # (you can think of `uselist` as a "list of children")
    child = db.relationship("Child", backref="parent", uselist=False)


class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    # If you go into your DB and modified it directly,
    # you will be able to create multiple Child records with the same parent_id.
    # But Flask-SQLAlchemy isn't going to do that.
    # If you do think you'll go through the DB,
    # adding `unique=True` to the following will make things safer.
    parent_id = db.Column(db.Integer, db.ForeignKey("parent.id"), unique=True)


if __name__ == "__main__":
    if os.path.exists(DB_FILE):
        print()
        print(f"found {os.path.abspath(DB_FILE)} - removing and re-creating it...")
        os.remove(DB_FILE)

    db.create_all()

    parent = Parent(name="Parent")
    child = Child(name="Child 1", parent=parent)
    db.session.add(parent)
    db.session.add(child)
    db.session.commit()

    child_2 = Child(name="Child 2", parent=parent)
    db.session.add(child_2)
    db.session.commit()
