from flask import Blueprint, request, jsonify
from datetime import datetime
from application.implemented import complaint_service
from implemented import user_service


api = Blueprint('api', __name__)


@api.route('/', methods=['GET', 'POST'], endpoint='api')
def api_order():
    if request.method == 'POST':
        data_received = request.form.to_dict()
        # print(data_received)
    if request.method == 'GET':
        data_received = request.values.get('str_item')
        order = data_received.split(';')
        order.remove('')
        print(order)
        for index, item in enumerate(order, start=100):
            data = {'print_order': index, 'id': item}
            complaint_service.update(data)

    return jsonify('ok')
