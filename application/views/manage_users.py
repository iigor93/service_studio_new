from services.decorators import auth_required, user_required
from flask import Blueprint, request, render_template, flash
from application.implemented import account_service
from datetime import datetime
from implemented import user_service
from application.services.check_user import check_user

manage_users = Blueprint('manage_users', __name__, template_folder='templates', static_folder='static')


@manage_users.route('/', methods=['GET', 'POST'], endpoint='all_users')
@user_required
def all_users():
    if request.method == 'POST':
        data_received = request.form.to_dict()

        if data_received.get('delete_user') == 'delete':
            user_service.delete(data_received.get('id'))

        if data_received.get('new_user_name'):
            new_user = {'username': data_received.get('new_user_name'),
                        'password': data_received.get('new_user_password'),
                        'role': data_received.get('new_user_role')}
            user_service.create(new_user)

    data = {'users_list': user_service.get_all()}
    admin = check_user()
    if admin:
        data['admin'] = admin.get('role')
        data['user_name'] = admin.get('user_name')
    else:
        data['user_name'] = 'no_user'
        data['admin'] = 'no_admin'
    return render_template('manage_user/manage_user.html', **data)
