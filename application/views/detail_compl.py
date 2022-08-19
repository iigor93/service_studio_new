from flask import Blueprint, render_template, request, redirect, url_for
from services.decorators import auth_required
from application.implemented import complaint_service
from application.implemented import account_service
from application.services.parsing import input_address
from datetime import datetime
from application.app_config import PRICE_DEFAULT, TRANSPORT_HOURS_DEFAULT
from application.views.complaint import check_user


detail_compl = Blueprint('detail_compl', __name__, template_folder='templates', static_folder='static')


@detail_compl.route('/<int:c_id>/', methods=['GET', 'POST'], endpoint='detail_compl')
@auth_required
def detail_view(c_id):
    if request.method == 'POST':
        data_received = request.form.to_dict()

        if data_received.get('additional_comment'):
            complaint_service.update(data_received)

        elif data_received.get('add_address'):
            new_address = {'address_complane': data_received.get('address') + ' ' + data_received.get('add_address'),
                           'id': data_received.get('id')}
            complaint_service.update(new_address)

        elif data_received.get('address'):
            corrected_address = input_address(data_received.get('address'))
            new_address = {'address_complane': corrected_address,
                           'id': data_received.get('id')}
            complaint_service.update(new_address)

        elif data_received.get('device_type'):
            complaint_service.update(data_received)

        elif data_received.get('status_complane'):
            data_received['account_id'] = 1
            format_ = "%Y-%m-%d"
            dt_object = datetime.strptime('1999-01-01', format_)
            data_received['date_at_work'] = dt_object
            complaint_service.update(data_received)

        elif data_received.get('delete_complane') == 'delete':
            complaint_service.delete(data_received.get('id'))
            return redirect(url_for('complaint.main'))

        elif data_received.get('date_at_work'):
            format_ = "%Y-%m-%d"
            dt_object = datetime.strptime(data_received.get('date_at_work'), format_)
            data_received['date_at_work'] = dt_object
            complaint_service.update(data_received)

        elif data_received.get('date_complited_real'):
            format_ = "%Y-%m-%d"
            dt_object = datetime.strptime(data_received.get('date_complited_real'), format_)
            data_received['date_complited_real'] = dt_object
            data_received['status_complane'] = 'done'
            complaint_service.update(data_received)

        elif data_received.get('transport_hours'):
            complaint_service.update(data_received)

        elif data_received.get('change_acc_for_complain'):
            data_received['account_id'] = data_received.get('change_acc_for_complain')
            data_received['price_status'] = PRICE_DEFAULT
            data_received['transport_hours'] = TRANSPORT_HOURS_DEFAULT
            complaint_service.update(data_received)

    data = {'print_view': 0, 'complane_view_all': 0, 'descr': 'Детальный вид',
            'date_time': datetime.now().date(), 'complain': complaint_service.get_one(c_id),
            'available_accounts': account_service.get_all_filter_closed()}

    admin = check_user()
    data['admin'] = 'admin' if admin else 'no_admin'
    return render_template('detail_compl/detail_c.html', **data)
