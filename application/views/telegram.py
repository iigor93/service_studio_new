from flask import Blueprint, request, jsonify
from datetime import datetime
from application.implemented import complaint_service
import json


tg = Blueprint('tg', __name__)


@tg.route('/', methods=['GET', 'POST'], endpoint='telegram')
def telegram():
    approved_users = {'igor': '717923644'}
    if request.method == 'POST':
        if request.is_json:
            json_message = request.json
            try:
                sender_id = json_message['message']['from'].get('id')
                sender_last_name = json_message['message']['from'].get('last_name')
                sender_text = json_message['message'].get('text')
                sender_chat_id = json_message['message']['chat'].get('id')
            except KeyError:
                return 200

            text_response = 'Сегодня ' + str(datetime.now().date())

            if sender_chat_id not in approved_users.values():
                chat_id = '717923644'
                text_response = sender_text
                sender_text = 'ddd'
            else:
                chat_id = sender_chat_id

            c_beg = str(sender_text)
            c_add = c_beg[1:]


            if sender_text == '1':
                text_response = 'С НОВЫМ ГОДОМ!'

            if c_beg[:1] == 'N' and len(c_beg) > 3:
                compl_list = complaint_service.get_all_filter(c_add)
                if len(compl_list) == 0:
                    text_response = 'Not found'
                else:
                    text_response = 'Кол-во: ' + str(len(compl_list)) + ' (' + str(datetime.now().date()) + ')' + '\r\n'
                    for lst in compl_list:
                        text_response += str(lst.numer_complane) + '_' + str(lst.client_phone_num) + '_' + str(lst.status_complane) + \
                                         '\r\n' + str(lst.address_complane) + \
                                         '\r\n' + str(lst.additional_comment) + '\r\n \r\n'

            if c_beg[:2] == 'At':

                compl_list = complaint_service.get_all_at_work()
                if len(compl_list) == 0:
                    text_response = 'Not found with status AT_WORK'
                else:
                    text_response = 'Кол-во: ' + str(len(compl_list)) + ' (' + str(
                        datetime.now().date()) + ')' + '\r\n'
                    for lst in compl_list:
                        text_response += str(lst.numer_complane) + '_' + str(lst.client_phone_num) + '_' + str(
                            lst.status_complane) + '\r\n(выезд: ' + str(lst.date_at_work) + ') \r\n' + str(
                            lst.address_complane) + '\r\n' + str(lst.additional_comment) + '\r\n \r\n'

            comment_var = ('_c_', '_с_', '_C_', '_С_')
            address_var = ('_a_', '_A_', '_а_', '_А_')
            help_var = ('Help', 'help')

            def is_dig(dig):
                for item in dig:
                    if item.isdigit() is False:
                        return False
                return True

            if c_beg[5:8].lower() in comment_var:
                if is_dig(c_beg[:5]):
                    complane_for_add = complaint_service.get_all_by_number(c_beg[:5])
                    if complane_for_add == 'Not found':
                        text_response = 'Рекламация не найдена'
                    else:
                        data = {'id': complane_for_add.id, 'additional_comment': str(complane_for_add.additional_comment) + ' ' + str(c_beg[7:])}
                        complaint_service.update(data)

                        text_response = f'Комментарий добавлен\r\n'
                        text_response += str(complane_for_add.numer_complane) + '_' + str(
                            complane_for_add.client_phone_num) + '_' + str(
                            complane_for_add.status_complane) + '_\r\n' + str(
                            complane_for_add.address_complane) + '_\r\n' + str(
                            complane_for_add.additional_comment) + '\r\n \r\n'

            if c_beg[5:8].lower() in address_var:
                if is_dig(c_beg[:5]):
                    complane_for_add = complaint_service.get_all_by_number(c_beg[:5])
                    if complane_for_add == 'Not found':
                        text_response = 'Рекламация не найдена'
                    else:
                        data = {'id': complane_for_add.id, 'address_complane': str(complane_for_add.address_complane) + ' ' + str(c_beg[7:])}
                        complaint_service.update(data)

                        text_response = f'Адрес добавлен\r\n'
                        text_response += str(complane_for_add.numer_complane) + '_' + str(
                            complane_for_add.client_phone_num) + '_' + str(
                            complane_for_add.status_complane) + '_\r\n' + str(
                            complane_for_add.address_complane) + '_\r\n' + str(
                            complane_for_add.additional_comment) + '\r\n \r\n'

            if c_beg in help_var:
                text_response = """
                XXXXX_c_добавить комментарий
                \r\nXXXXX_a_добавить адрес
                \r\nNXXX - поиск по номеру рекламации или тел
                \r\nAt - все рекламации со статусом в работе"""

            response = jsonify({'code': 200, 'method': 'sendMessage', 'chat_id': chat_id, 'text': text_response})

            return response
        else:
            return 200
