from services.decorators import auth_required
from flask import Blueprint, request, render_template, redirect, url_for, flash
from application.implemented import complaint_service
from application.services.parsing import parsing_from_input, parsing_from_input_bitrix, hand_input_parsing
from datetime import datetime, timedelta
from application.services.check_user import check_user


complaint = Blueprint('complaint', __name__, template_folder='templates', static_folder='static')


@complaint.route('/', methods=['GET', 'POST'], endpoint='main')
@auth_required
def main():
    data = {'print_view': 0, 'complane_view_all': 0}
    if request.method == 'POST':
        data_received = request.form.to_dict()

        if data_received.get('find_smth'):
            """ Поиск """
            search = data_received.get('find_smth')
            if len(search) > 2:
                data['complane_list'] = complaint_service.get_all_filter(search)
                data['descr'] = 'ПОИСК'
                admin = check_user()
                if admin:
                    data['admin'] = admin.get('role')
                    data['user_name'] = admin.get('user_name')
                else:
                    data['user_name'] = 'no_user'
                    data['admin'] = 'no_admin'
                return render_template('complaint/complaint.html', **data)

        elif data_received.get('complaint'):
            """ Новая рекламация """
            if data_received.get('Bitrix24'):
                data = parsing_from_input_bitrix(data_received.get('complaint'))
            else:
                data = parsing_from_input(data_received.get('complaint'))
            flash(complaint_service.create(data))

        elif data_received.get('hand_compl_num'):
            """ Ручной ввод рекламации """
            data = hand_input_parsing(data_received)
            flash(complaint_service.create(data))
            pass

        elif data_received.get('status_complane'):
            complaint_service.update(data_received)

        return redirect(url_for('complaint.main'))

    data['complane_list'] = complaint_service.get_all()
    data['descr'] = 'Новые рекламации'
    admin = check_user()
    if admin:
        data['admin'] = admin.get('role')
        data['user_name'] = admin.get('user_name')
    else:
        data['user_name'] = 'no_user'
        data['admin'] = 'no_admin'

    return render_template('complaint/complaint.html', **data)


@complaint.route('/at_work/', methods=['GET', 'POST'], endpoint='at_work')
@auth_required
def at_work():
    data = {'print_view': 1, 'complane_view_all': 0, 'descr': 'В Работе'}
    if request.method == 'POST':
        data_received = request.form.to_dict()
        if data_received.get('print_order'):
            complaint_service.update(data_received)

    data['all_dates_at_work'] = sorted(list(complaint_service.all_dates_at_work()), reverse=True)
    data['req'] = str(datetime.now().date() + timedelta(days=1))

    if request.args.get('dt'):
        data['complane_list'] = complaint_service.get_all_at_work_with_date(request.args.get('dt'))
        data['req'] = request.args.get('dt')
    else:
        pass  # data['complane_list'] = complaint_service.get_all_at_work()

    admin = check_user()
    if admin:
        data['admin'] = admin.get('role')
        data['user_name'] = admin.get('user_name')
    else:
        data['user_name'] = 'no_user'
        data['admin'] = 'no_admin'
    return render_template('complaint/complaint.html', **data)
