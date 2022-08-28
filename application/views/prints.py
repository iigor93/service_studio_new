from services.decorators import auth_required
from flask import Blueprint, request, render_template, redirect, url_for
from application.implemented import complaint_service
from application.services.account_calculation import account_calculation


prints = Blueprint('prints', __name__, template_folder='templates', static_folder='static')


@prints.route('/', methods=['GET', 'POST'], endpoint='print_all')
@auth_required
def print_all():
    if request.method == 'POST':
        data_received = request.form.to_dict()
        dt_object = data_received.get('date_print')
        c_date_show = data_received.get('dt') + ' 00:00:00'

        c_list_new = complaint_service.get_all_at_work_with_date(c_date_show)

        if len(c_list_new) == 0:
            c_list_new = {'ne': 'ne'}
        else:
            for item in c_list_new:
                item.description_complane = item.description_complane.replace('(HE)', '')
        data = {'complane_list': c_list_new, 'date_time': dt_object, 'full_empty': 'on'}
        return render_template('complaint/new2.htm', **data)
    return redirect(url_for('complaint.at_work'))


@prints.route('/print_one', methods=['GET', 'POST'], endpoint='print_one')
@auth_required
def print_one():
    if request.method == 'POST':
        data_received = request.form.to_dict()
        dt_object = data_received.get('date_print')
        id_ = data_received.get('id_')
        full_empty = data_received.get('empty')

        c_list_new = [complaint_service.get_one(id_)]

        if len(c_list_new) == 0:
            c_list_new = {'ne': 'ne'}
        data = {'complane_list': c_list_new, 'date_time': dt_object, 'full_empty': full_empty}
        return render_template('complaint/new2.htm', **data)
    return redirect(url_for('complaint.at_work'))


@prints.route('/empty', methods=['GET', 'POST'], endpoint='print_empty')
@auth_required
def print_empty():
    c_list_new = {'ne': 'ne'}
    data_received = request.form.to_dict()
    full_empty = data_received.get('empty')
    data = {'complane_list': c_list_new, 'printEmpty': 1, 'full_empty': full_empty}
    return render_template('complaint/new2.htm', **data)


@prints.route('/account_print', methods=['GET', 'POST'], endpoint='account_print')
@auth_required
def account_print():
    if request.method == 'POST':
        data_received = request.form.to_dict()
        data = account_calculation(data_received.get('id'))

        return render_template('account/account_print.html', **data)
    return redirect(url_for('account.all_accounts'))
