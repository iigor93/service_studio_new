import jwt
from flask import session
from config import ALGO, SECRET
from implemented import user_service


def check_user():
    access_token = session.get('access_token')
    try:
        user = jwt.decode(access_token, SECRET, algorithms=[ALGO])
        user_name = user_service.get_one(user.get('user_id'))

        return {'user_name': user_name.username, 'role': user_name.role}
    except:  # Exception as e:
        return False
