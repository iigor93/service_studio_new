from flask import redirect, url_for
from services.tokens import check_tokens, check_user


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
