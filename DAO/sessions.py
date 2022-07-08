from DAO.Models.sessions import Session


class SessionDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(Session).get(bid)

    def get_all_filter(self, refresh_token):
        return self.session.query(Session).filter(Session.refresh_token == refresh_token).first()

    def get_all_by_uid(self, uid):
        return self.session.query(Session).filter(Session.user_id == int(uid)).all()

    def get_all(self):
        return self.session.query(Session).all()

    def create(self, session_new):
        ent = Session(**session_new)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, rid):
        sess = self.get_one(rid)
        self.session.delete(sess)
        self.session.commit()

    def update(self, session_d):
        sess = self.get_one(session_d.get("id"))
        if session_d.get("access_token"):
            sess.access_token = session_d.get("access_token")
        if session_d.get("refresh_token"):
            sess.refresh_token = session_d.get("refresh_token")
        if session_d.get("user_id"):
            sess.user_id = session_d.get("user_id")
        if session_d.get("expiry_date_unix"):
            sess.expiry_date_unix = session_d.get("expiry_date_unix")

        self.session.add(sess)
        self.session.commit()

