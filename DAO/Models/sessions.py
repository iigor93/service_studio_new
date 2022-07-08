"""Sessions models"""
from db_config import db


class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String)
    refresh_token = db.Column(db.String)
    user_id = db.Column(db.Integer)
    expiry_date_unix = db.Column(db.Integer)
