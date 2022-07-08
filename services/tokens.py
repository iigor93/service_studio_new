import jwt
import datetime
import calendar
from config import ACCESS_TOKEN_LIFE, REFRESH_TOKEN_LIFE, ALGO, SECRET
from flask import session, redirect, url_for
from implemented import session_service, user_service
from services.session_update import session_update


def generate_tokens(user):
    data = {'user_id': user.id, 'role': user.role}

    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_LIFE)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, SECRET, algorithm=ALGO)

    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=REFRESH_TOKEN_LIFE)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, SECRET, algorithm=ALGO)

    return {"access_token": access_token, "refresh_token": refresh_token, "refresh_token_exp": data.get('exp')}


def check_tokens():
    access_token = session.get('access_token')
    refresh_token = session.get('refresh_token')
    if access_token:
        try:
            user = jwt.decode(access_token, SECRET, algorithms=[ALGO])
        except jwt.exceptions.ExpiredSignatureError as e:  # Exception as e:
            print("JWT Decode Exception, access_token", e)
            try:
                user_refresh = jwt.decode(refresh_token, SECRET, algorithms=[ALGO])
                db_token = session_service.get_all_filter(refresh_token)
                if db_token:
                    session_service.delete(db_token.id)
                    user = user_service.get_one(user_refresh.get('user_id'))
                    tokens = generate_tokens(user)
                    session_update(tokens, user)
                else:
                    all_user_tokens = session_service.get_all_by_uid(user_refresh.get('user_id'))
                    for item in all_user_tokens:
                        session_service.delete(item.id)
                    return False

            except jwt.exceptions.ExpiredSignatureError as e:
                print("JWT Decode Exception, refresh_token", e)
                return False
        return True
    return False

