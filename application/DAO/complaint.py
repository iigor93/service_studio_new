from application.DAO.Models.complaint import Complaint
from sqlalchemy import or_, and_, exc
from datetime import datetime



class ComplaintDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(Complaint).get(bid)

    def get_all_by_number(self, number):
        try:
            item = self.session.query(Complaint).filter(Complaint.numer_complane == number).one()
        except exc.NoResultFound:
            item = 'Not found'
        return item

    def get_all_filter(self, search_data):
        search_data = search_data.strip()
        return self.session.query(Complaint).filter(or_(Complaint.numer_complane.like(f'%{search_data}%'),
                                                        Complaint.client_phone_num.like(f'%{search_data}%'),
                                                        Complaint.address_complane.like(f'%{search_data}%'),
                                                        )).all()

    def get_all(self):
        return self.session.query(Complaint).filter(Complaint.status_complane != 'done').\
            order_by(Complaint.device_type, Complaint.numer_complane.desc()).all()

    def get_all_for_check(self):
        return self.session.query(Complaint).all()

    def get_all_at_work(self):
        return self.session.query(Complaint).filter(Complaint.status_complane == 'at_work').\
            order_by(Complaint.print_order).all()

    def get_all_at_work_with_dates(self, dt):
        format_ = "%Y-%m-%d %H:%M:%S"
        dt_object = datetime.strptime(dt, format_)
        return self.session.query(Complaint).filter(and_(Complaint.date_at_work == dt_object,
                                                         Complaint.status_complane == 'at_work'))\
            .order_by(Complaint.print_order).all()

    def create(self, complaint_d):
        ent = Complaint(**complaint_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, rid):
        account = self.get_one(rid)
        self.session.delete(account)
        self.session.commit()

    def update(self, complaint_d):
        complaint = self.get_one(complaint_d.get("id"))
        if complaint_d.get("account_id"):
            complaint.account_id = complaint_d.get("account_id")
        if complaint_d.get("numer_complane"):
            complaint.numer_complane = complaint_d.get("numer_complane")
        if complaint_d.get("date_creation"):
            complaint.date_creation = complaint_d.get("date_creation")
        if complaint_d.get("date_complited_real"):
            complaint.date_complited_real = complaint_d.get("date_complited_real")
        if complaint_d.get("date_complited_fake"):
            complaint.date_complited_fake = complaint_d.get("date_complited_fake")
        if complaint_d.get("status_complane"):
            complaint.status_complane = complaint_d.get("status_complane")
        if complaint_d.get("description_complane"):
            complaint.description_complane = complaint_d.get("description_complane")
        if complaint_d.get("address_complane"):
            complaint.address_complane = complaint_d.get("address_complane")
        if complaint_d.get("client_name"):
            complaint.client_name = complaint_d.get("client_name")
        if complaint_d.get("client_phone_num"):
            complaint.client_phone_num = complaint_d.get("client_phone_num")

        if complaint_d.get("client_email"):
            complaint.client_email = complaint_d.get("client_email")

        if complaint_d.get("device_type"):
            complaint.device_type = complaint_d.get("device_type")
        if complaint_d.get("additional_comment"):
            complaint.additional_comment = complaint_d.get("additional_comment")
        if complaint_d.get("transport_hours"):
            complaint.transport_hours = complaint_d.get("transport_hours")
        if complaint_d.get("print_order"):
            complaint.print_order = complaint_d.get("print_order")
        if complaint_d.get("price_status"):
            complaint.price_status = complaint_d.get("price_status")
        if complaint_d.get("date_at_work"):
            complaint.date_at_work = complaint_d.get("date_at_work")
        if complaint_d.get("filename"):
            complaint.filename = complaint_d.get("filename")

        self.session.add(complaint)
        self.session.commit()
