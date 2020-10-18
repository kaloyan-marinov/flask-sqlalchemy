import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


DB_FILE = os.path.splitext(__file__)[0] + ".db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_FILE}"
db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = "persons"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    pets = db.relationship("Pet", backref="owner")

    def __repr__(self):
        return f"<Person (name={self.name})>"


class Pet(db.Model):
    __tablename__ = "pets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    owner_id = db.Column(db.Integer, db.ForeignKey("persons.id"))

    def __repr__(self):
        return f"<Pet (name={self.name}, owner_id={self.owner_id})>"


if __name__ == "__main__":
    if os.path.exists(DB_FILE):
        print()
        print(f"found {os.path.abspath(DB_FILE)} - removing and re-creating it...")
        os.remove(DB_FILE)

    db.create_all()

    anthony = Person(name="Anthony")
    db.session.add(anthony)
    db.session.commit()

    michelle = Person(name="Michelle")
    db.session.add(michelle)
    db.session.commit()

    spot = Pet(name="Spot", owner=anthony)
    db.session.add(spot)
    db.session.commit()

    brian = Pet(name="Brian", owner=michelle)
    db.session.add(brian)
    db.session.commit()

    clifford = Pet(name="Clifford", owner=anthony)
    db.session.add(clifford)
    db.session.commit()

    print()
    for owner in [anthony, michelle]:
        print(f"{owner.name} has the following pets: {owner.pets}")

    print()
    print(f"The owner of {spot.name} is {spot.owner}")
