from db_config import db


class Account(db.Model):
	__tablename__ = 'account'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	account_number = db.Column(db.String)
	account_date = db.Column(db.DateTime)
	account_price = db.Column(db.String)
	account_paid = db.Column(db.Boolean, nullable=True)
	#complaint = db.relationship("Complaint")
