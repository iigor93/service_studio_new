import os
import zipfile

import config
from services.decorators import user_required
from flask import Blueprint, request, render_template, flash, send_file
from application.implemented import account_service
from datetime import datetime
from application.services.add_comp_to_account import compl_to_account
from application.services.check_user import check_user


account = Blueprint('account', __name__, template_folder='templates', static_folder='static')


@account.route('/', methods=['GET', 'POST'], endpoint='all_accounts')
@user_required
def all_accounts():
    date_time = datetime.now().date()
    data = {'descr': 'Счета', 'date_time': date_time}
    if request.method == 'POST':
        data_received = request.form.to_dict()
        data = {'account_number': data_received.get('account_number'),
                'account_date': datetime.now().date(),
                'account_price': 0,
                'account_paid': False}
        account_service.create(data)
    data['account_list'] = account_service.get_all()
    admin = check_user()
    if admin:
        data['admin'] = admin.get('role')
        data['user_name'] = admin.get('user_name')
    else:
        data['user_name'] = 'no_user'
        data['admin'] = 'no_admin'
    return render_template('account/account.html', **data)


@account.route('/<int:aid>/', methods=['GET', 'POST'], endpoint='account_details')
@user_required
def account_details(aid):
    if request.method == 'POST':
        data_received = request.form.to_dict()
        if data_received.get('account_paid'):
            if data_received.get('account_paid') == 'on':
                data_received['account_paid'] = 1
            else:
                data_received['account_paid'] = 0
            account_service.update(data_received)

        elif data_received.get('account_date'):
            data_received['account_date'] += ' 00:00:00'
            format_ = "%Y-%m-%d %H:%M:%S"
            dt_object = datetime.strptime(data_received['account_date'], format_)
            data_received['account_date'] = dt_object
            account_service.update(data_received)

        elif data_received.get('compl_list'):
            flash(compl_to_account(data_received.get('compl_list'), data_received.get('id')))

    account_ = account_service.get_one(aid)
    data = {'descr': 'Детальный вид счета', 'account': account_, 'date_time': datetime.now().date()}
    admin = check_user()
    if admin:
        data['admin'] = admin.get('role')
        data['user_name'] = admin.get('user_name')
    else:
        data['user_name'] = 'no_user'
        data['admin'] = 'no_admin'
    return render_template('account/detail.html', **data)


@account.route('/<int:aid>/download/', methods=['GET'], endpoint='account_download_pic')
@user_required
def account_details(aid):
    account_ = account_service.get_one(aid)

    files_to_zip = [os.path.join(config.UPLOAD_FOLDER, complaint.filename)
                    for complaint in account_.complaint if complaint.filename]

    temp_dir = os.path.join(config.UPLOAD_FOLDER, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    zip_filename = os.path.join(temp_dir, f'счет №{account_.account_number}.zip')
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for path in files_to_zip:
            file_name = os.path.basename(path)
            zip_file.write(path, file_name)

    return send_file(zip_filename, as_attachment=True)
