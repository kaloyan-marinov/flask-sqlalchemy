"""
The main thing you need to know when creating a many-to-many relationship
in a relational database is that you need an auxiliary table
to associate the primary keys in one of the tables to primary keys in the other table.
Such an auxiliary table is (fittingly!) called an "association table".

example 1: TV channels that different customers are subscribed to
example 2: courses that different students are enrolled in
"""

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


DB_FILE = os.path.splitext(__file__)[0] + ".db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_FILE}"
db = SQLAlchemy(app)


customer_channel_pairs = db.Table(
    "customer_channel_pairs",
    db.Column("customer_id", db.Integer, db.ForeignKey("customers.id")),
    db.Column("channel_id", db.Integer, db.ForeignKey("channels.id")),
)


class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    subscriptions = db.relationship(
        "Channel",
        secondary="customer_channel_pairs",
        backref=db.backref("subscribers", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<Customer (name={self.name})>"


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

    customer_1 = Customer(name="Adam")
    customer_2 = Customer(name="Bob")
    customer_3 = Customer(name="Charlie")
    customer_4 = Customer(name="David")
    db.session.add(customer_1)
    db.session.add(customer_2)
    db.session.add(customer_3)
    db.session.add(customer_4)
    db.session.commit()

    channel_1 = Channel(name="Traversy Media")
    channel_2 = Channel(name="Pretty Printed")
    db.session.add(channel_1)
    db.session.add(channel_2)
    db.session.commit()

    channel_1.subscribers.append(customer_1)
    channel_1.subscribers.append(customer_3)
    channel_1.subscribers.append(customer_4)
    channel_2.subscribers.append(customer_2)
    channel_2.subscribers.append(customer_4)
    db.session.commit()

    for c in [channel_1, channel_2]:
        print()
        print(type(c.subscribers))
        for u in c.subscribers:
            print(f"{u} is subscribed to {c}")
