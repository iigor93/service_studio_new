from flask import Blueprint, render_template_string, request, abort, session, redirect, url_for
from services.check_user_in_db import user_check_in_db
from services.tokens import generate_tokens
from services.session_update import session_update
from services.decorators import auth_required
from implemented import session_service


login_logout = Blueprint('login_logout', __name__)


@login_logout.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input = request.form['input_username']
        password_input = request.form['password_input']
        user = user_check_in_db(user_input, password_input)

        if user:
            tokens = generate_tokens(user)
            session_update(tokens, user)
            return redirect(url_for('complaint.main'))
        return abort(401)

    return render_template_string("""
            <form method="post">
                <label for="input">Enter your login and password:</label><br>
                <input type="input" id="input" name="input_username" required /><br>
                <input type="password" id="password" name="password_input" required/> <br>
                <button type="submit">Login</button>
            </form><br>""")


@login_logout.route('/logout', endpoint='logout')
@auth_required
def logout():
    refresh_token = session.get('refresh_token')
    session.pop('access_token', default=None)
    session.pop('refresh_token', default=None)
    db_token = session_service.get_all_filter(refresh_token)
    session_service.delete(db_token.id)
    return f'<h1>Session deleted!<br>{url_for("complaint.main")}</h1>'
