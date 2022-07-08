from db_config import db
from application.DAO.Models.account import Account


class Complaint(db.Model):
    __tablename__ = 'complaint'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    accounts = db.relationship("Account", backref='complaint')
    numer_complane = db.Column(db.String)
    date_creation = db.Column(db.String)
    date_complited_real = db.Column(db.String)
    date_complited_fake = db.Column(db.String)
    status_complane = db.Column(db.String)  # статус NEW, at_work, done
    description_complane = db.Column(db.String)
    address_complane = db.Column(db.String)
    client_name = db.Column(db.String)
    client_phone_num = db.Column(db.String)
    client_email = db.Column(db.String)
    device_type = db.Column(db.String)
    additional_comment = db.Column(db.String)  # доп информация. типа зайти после 14.00
    print_order = db.Column(db.String)  # порядок сортировки для печати
    price_status = db.Column(db.Integer, nullable=True)  # Стоимость одной заявки - индекс. в счете выставляется нужная сумма
    transport_hours = db.Column(db.Integer, nullable=True)  # количество часов дороги, для оплаты
    date_at_work = db.Column(db.DateTime, nullable=True)  # Дата когда планируется выезд
