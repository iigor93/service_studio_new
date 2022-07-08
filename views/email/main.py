from flask import Blueprint, request, session, redirect, render_template_string
from implemented import session_service
from services.decorators import auth_required


email = Blueprint('email', __name__)


@email.route('/set', methods=['GET', 'POST'])
def set_email():
    if request.method == 'POST':
        # Save the form data to the session object
        session['email'] = request.form['email_address']
        session['access_token'] = 'kkk'
        session.permanent = True
        data = {
            'access_token': 'access_token',
            'refresh_token': 'dddd',
            'user_id': 1,
            'expiry_date_unix': 1
        }
        session_service.create(data)
        return redirect('./get')

    return render_template_string("""
        <form method="post">
            <label for="email">Enter your email address:</label>
            <input type="email" id="email" name="email_address" required />
            <button type="submit">Submit</button>
        </form><br>
        {% if session['email'] %}
            <h1>Welcome {{ session['email'] }}!</h1>
        {% else %}
            <h1>Welcome! Please enter your email <a href="{{ url_for('email.set_email') }}">here.</a></h1>
        {% endif %}
        """)


@email.route('/get', endpoint='get_email')
@auth_required
def get_email():
    return render_template_string("""
                {% if session['email'] %}
                    <h1>Welcome {{ session['email'] }}!</h1>
                {% else %}
                    <h1>Welcome! Please enter your email <a href="{{ url_for('email.set_email') }}">here.</a></h1>
                {% endif %}
            """)


@email.route('/delete', endpoint='delete_email')
@auth_required
def delete_email():
    # Clear the email stored in the session object
    session.pop('email', default=None)
    session.pop('access_token', default=None)
    return '<h1>Session deleted!</h1>'
