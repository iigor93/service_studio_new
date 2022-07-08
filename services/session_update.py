from flask import session
from implemented import session_service


def session_update(tokens, user):
    session['access_token'] = tokens.get('access_token')
    session['refresh_token'] = tokens.get('refresh_token')
    session.permanent = True
    data = {
        'access_token': tokens.get('access_token'),
        'refresh_token': tokens.get('refresh_token'),
        'user_id': user.id,
        'expiry_date_unix': tokens.get('refresh_token_exp')
    }
    session_service.create(data)
