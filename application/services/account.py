from application.DAO.account import AccountDAO


class AccountService:
    def __init__(self, dao: AccountDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self):
        return self.dao.get_all()

    def get_all_filter(self, numer_complane):
        return self.dao.get_all_filter(numer_complane)

    def get_all_filter_closed(self):
        return self.dao.get_all_filter_closed()

    def create(self, complaint_d):
        return self.dao.create(complaint_d)

    def update(self, complaint_d):
        self.dao.update(complaint_d)
        return self.dao

    def delete(self, rid):
        self.dao.delete(rid)
