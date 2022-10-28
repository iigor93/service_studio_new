from flask import Blueprint, request, jsonify
from datetime import datetime
from application.implemented import complaint_service
from application.services.parsing import input_address
from implemented import user_service


api = Blueprint('api', __name__)


@api.route('/', methods=['GET', 'POST'], endpoint='api')
def api_order():
    if request.method == 'POST':
        data_received = request.form.to_dict()
        # print(data_received)
        id_ = int(data_received.get('id').split('__')[1])
        attr = data_received.get('id').split('__')[0]
        value = data_received.get('value')

        data = {'id': id_, attr: value}

        additional_comment = ''
        address = ''

        if attr == 'additional_comment':
            complaint_service.update(data)
            additional_comment = value

        elif attr == 'add_address':
            current_address = complaint_service.get_one(id_).address_complane
            # print(current_address)
            new_address = {'address_complane': current_address + ' ' + data.get('add_address'),
                           'id': data.get('id')}
            complaint_service.update(new_address)
            address = current_address + ' ' + data.get('add_address')

        elif attr == 'address':
            corrected_address = input_address(value)
            new_address = {'address_complane': corrected_address,
                           'id': data.get('id')}
            complaint_service.update(new_address)
            address = corrected_address

        data_return = {'additional_comment': additional_comment,
                       'address': address}

        return jsonify(data_return)

    if request.method == 'GET':
        data_received = request.values.get('str_item')
        order = data_received.split(';')
        order.remove('')
        # print(order)
        for index, item in enumerate(order, start=100):
            data = {'print_order': index, 'id': item}
            complaint_service.update(data)

        return jsonify('ok')
