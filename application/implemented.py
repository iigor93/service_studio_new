from application.DAO.account import AccountDAO
from application.DAO.complaint import ComplaintDAO

from application.services.account import AccountService
from application.services.complaint import ComplaintService
from db_config import db


account_dao = AccountDAO(session=db.session)
complaint_dao = ComplaintDAO(session=db.session)
account_service = AccountService(dao=account_dao)
complaint_service = ComplaintService(dao=complaint_dao)