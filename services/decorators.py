from flask import abort, session, redirect, url_for
from config import ALGO, SECRET
import jwt
from services.tokens import generate_tokens, check_tokens, check_user
from implemented import user_service, session_service
from services.session_update import session_update


def auth_required(func):
    def wrapper(*args, **kwargs):
        if check_tokens():
            return func(*args, **kwargs)
        return redirect(url_for('login_logout.login'))

    return wrapper


def user_required(func):
    def wrapper(*args, **kwargs):
        if check_user():
            return func(*args, **kwargs)
        return redirect(url_for('login_logout.login'))

    return wrapper
