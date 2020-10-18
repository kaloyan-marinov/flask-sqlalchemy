"""
The main thing you need to know when creating a many-to-many relationship
in a relational database is that you need an auxiliary table
to associate the primary keys in one of the tables to primary keys in the other table.
Such an auxiliary table is (fittingly!) called an "association table".

example 1: TV channels that different users are subscribed to
example 2: courses that different students are enrolled in
"""

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


DB_FILE = os.path.splitext(__file__)[0] + ".db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_FILE}"
db = SQLAlchemy(app)


user_channel_association_table = db.Table(
    "user_channel_association_table",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("channel_id", db.Integer, db.ForeignKey("channels.id")),
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    subscriptions = db.relationship(
        "Channel",
        secondary="user_channel_association_table",
        backref=db.backref("subscribers", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<User (name={self.name})>"


class Channel(db.Model):
    __tablename__ = "channels"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    def __repr__(self):
        return f"<Channel (id={self.id}, name={self.name})>"


if __name__ == "__main__":
    if os.path.exists(DB_FILE):
        print()
        print(f"found {os.path.abspath(DB_FILE)} - removing and re-creating it ...")
        os.remove(DB_FILE)

    db.create_all()

    user_1 = User(name="Adam")
    user_2 = User(name="Bob")
    user_3 = User(name="Charlie")
    user_4 = User(name="David")
    db.session.add(user_1)
    db.session.add(user_2)
    db.session.add(user_3)
    db.session.add(user_4)
    db.session.commit()

    channel_1 = Channel(name="Traversy Media")
    channel_2 = Channel(name="Pretty Printed")
    db.session.add(channel_1)
    db.session.add(channel_2)
    db.session.commit()

    channel_1.subscribers.append(user_1)
    channel_1.subscribers.append(user_3)
    channel_1.subscribers.append(user_4)
    channel_2.subscribers.append(user_2)
    channel_2.subscribers.append(user_4)
    db.session.commit()

    for c in [channel_1, channel_2]:
        print()
        print(type(c.subscribers))
        for u in c.subscribers:
            print(f"{u} is subscribed to {c}")
