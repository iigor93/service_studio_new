from DAO.sessions import SessionDAO


class SessionService:
    def __init__(self, dao: SessionDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self):
        return self.dao.get_all()

    def get_all_filter(self, refresh_token):
        return self.dao.get_all_filter(refresh_token)

    def get_all_by_uid(self, uid):
        return self.dao.get_all_by_uid(uid)

    def create(self, session_d):
        # user_d['password'] = get_hash(user_d.get('password'))
        return self.dao.create(session_d)

    def update(self, session_d):
        # user_d['password'] = get_hash(user_d.get('password'))
        self.dao.update(session_d)
        return self.dao

    def delete(self, rid):
        self.dao.delete(rid)
