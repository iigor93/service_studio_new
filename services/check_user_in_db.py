from implemented import user_service
from services.users import get_hash
import hmac


def user_check_in_db(username, password):
    """Проверка пользователя и пароля в БД"""
    users = user_service.get_all_filter(username)
    if users:
        for user in users:
            if hmac.compare_digest(user.password.encode('utf-8'), get_hash(password).encode('utf-8')):
                return user
    return False
