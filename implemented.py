from DAO.sessions import SessionDAO
from DAO.users import UserDAO
from services.sessions import SessionService
from services.users import UserService
from db_config import db


session_dao = SessionDAO(session=db.session)
user_dao = UserDAO(session=db.session)
session_service = SessionService(dao=session_dao)
user_service = UserService(dao=user_dao)
