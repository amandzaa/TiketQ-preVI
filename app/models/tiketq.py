from ..extensions import db

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eventName = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    isUsed = db.Column(db.Boolean, default=False, nullable=False) 