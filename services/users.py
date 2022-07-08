from DAO.users import UserDAO
from config import PWD_HASH_SALT, PWD_HASH_ITERATIONS
import hashlib


def get_hash(password):
    """ Генерация hash для пароля пользователя"""
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS
    ).decode('utf-8', 'ignore')


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all_filter(self, username):
        return self.dao.get_all_filter(username)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_d):
        user_d['password'] = get_hash(user_d.get('password'))
        return self.dao.create(user_d)

    def update(self, user_d):
        user_d['password'] = get_hash(user_d.get('password'))
        self.dao.update(user_d)
        return self.dao

    def delete(self, rid):
        self.dao.delete(rid)
