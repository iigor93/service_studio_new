from markupsafe import Markup

from application.DAO.complaint import ComplaintDAO


class ComplaintService:
    def __init__(self, dao: ComplaintDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self):
        return self.dao.get_all()

    def get_all_for_check(self):
        return self.dao.get_all_for_check()

    def get_all_at_work(self):
        return self.dao.get_all_at_work()

    def get_all_filter(self, account_number):
        return self.dao.get_all_filter(account_number)

    def get_all_by_number(self, number):
        return self.dao.get_all_by_number(number)

    def create(self, account_d):
        if account_d.get('numer_complane') == '':
            return 'Не верный формат записи'
        if account_d.get('numer_complane') != 'N/A':
            all_complaints = self.get_all_for_check()
            for item in all_complaints:
                if item.numer_complane == account_d.get('numer_complane'):
                    return f'Рекламация с таким номером ({account_d.get("numer_complane")}) уже существует'
        self.dao.create(account_d)
        msg = f'Рекламация {account_d.get("numer_complane")} создана<br>'
        msg += f'Address: {account_d.get("address_complane")}<br>'
        msg += f'Name: {account_d.get("client_name")}<br>'
        msg += f'Phone: {account_d.get("client_phone_num")}<br>'
        msg += f'Description: {account_d.get("description_complane")}<br>'
        return Markup(msg)

    def all_dates_at_work(self):
        all_dates = []
        all_complaints_at_work = self.get_all_at_work()
        for item in all_complaints_at_work:
            if item.date_at_work not in all_dates and item.date_at_work is not None:
                all_dates.append(item.date_at_work)
        return all_dates

    def get_all_at_work_with_date(self, dt):
        return self.dao.get_all_at_work_with_dates(dt)

    def update(self, account_d):
        self.dao.update(account_d)
        return self.dao

    def delete(self, rid):
        self.dao.delete(rid)
