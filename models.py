from django import db
from app import db
from datetime import datetime


class ToDoTable(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    desc = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


class Students(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(200))
    lastName = db.Column(db.String(500))
    age = db.Column(db.Integer)

# Run below command to generate tables
# db.create_all()
