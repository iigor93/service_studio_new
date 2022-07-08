from application.DAO.Models.account import Account


class AccountDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(Account).get(bid)

    def get_all_filter(self, account_number):
        return self.session.query(Account).filter(Account.account_number == account_number).all()

    def get_all(self):
        return self.session.query(Account).order_by(Account.account_paid, Account.account_date.desc()).all()

    def get_all_filter_closed(self):
        return self.session.query(Account).filter(Account.account_paid == False)

    def create(self, account_d):
        ent = Account(**account_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, rid):
        account = self.get_one(rid)
        self.session.delete(account)
        self.session.commit()

    def update(self, account_d):
        account = self.get_one(account_d.get("id"))
        if account_d.get("account_date"):
            account.account_date = account_d.get("account_date")
        if account_d.get("account_price"):
            account.account_price = account_d.get("account_price")
        if account_d.get("account_paid") == 1:
            account.account_paid = True
        elif account_d.get("account_paid") == 0:
            account.account_paid = False

        if account_d.get("account_number"):
            account.account_number = account_d.get("account_number")

        self.session.add(account)
        self.session.commit()
