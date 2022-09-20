from datetime import date
from dadata import Dadata
from config import DADATA_TOKEN, DADATA_SECRET


def parsing_from_input_bitrix(user_input):
    """Takes data from user input textarea"""
    malfunction = 'Неисправность'
    address_complaint = 'Адрес полностью, где находится оборудование'
    phone_ = 'Контактный мобильный телефон'
    person_ = 'ФИО полностью'
    sn_ = 'Серийный номер'
    new_data = {}

    complaint_num = user_input[
                    user_input.find('НЕ-'):
                    user_input.find('\r\n', user_input.find('НЕ-'))
                    ]
    if user_input.find('НЕ-') == -1:
        new_data['numer_complane'] = ''
    else:
        new_data['numer_complane'] = complaint_num.strip()

    new_data['account_id'] = 1

    complaint_date_start = user_input.find('Ждет выполнения с ') + 18
    complaint_date = user_input[complaint_date_start: complaint_date_start + 10]  # Дата заявки
    new_data['date_creation'] = complaint_date
    new_data['date_complited_real'] = complaint_date

    c_files_user = str(user_input.find('Файлы:'))
    new_data['date_complited_fake'] = '1'
    if c_files_user == '-1':
        new_data['date_complited_fake'] = '0'

    complaint_phone = user_input[
                      user_input.find(phone_) + len(phone_):
                      user_input.find('\r\n', (user_input.find(phone_)))
                      ]
    tp = complaint_phone.replace("-", "").replace("(", "").replace(")", "").strip()
    if '@' in tp:
        tp = tp.split(' ')
        tp.pop()
        tp = ''.join(tp)
    tp = tp.replace(" ", "")
    new_data['client_phone_num'] = tp
    if len(tp) == 10:  # without +7 or 8 or 7 at begin
        new_data['client_phone_num'] = f'+7({tp[0:3]}){tp[3:6]}-{tp[6:10]}'
    if len(tp) == 11:  # 8 999 123 4567
        if tp[0] == '8':
            new_data['client_phone_num'] = f'+7({tp[1:4]}){tp[4:7]}-{tp[7:11]}'
        else:
            new_data['client_phone_num'] = f'{tp[0]}({tp[1:4]}){tp[4:7]}-{tp[7:11]}'
    if len(tp) == 12:  # +7 999 123 4567
        new_data['client_phone_num'] = f'{tp[0:2]}({tp[2:5]}){tp[5:8]}-{tp[8:12]}'

    c_address = user_input[user_input.find(address_complaint) + len(address_complaint):
                           user_input.find('\r\n', (user_input.find(address_complaint)))]
    c_address = str(input_address(c_address))  # Dadata address correction
    new_data['address_complane'] = c_address

    new_data['device_type'] = type_by_address(c_address)

    desc_one = user_input[user_input.find(malfunction) + len(malfunction):
                          user_input.find('\r\n', user_input.find(malfunction))]

    desc_two = user_input[user_input.find(sn_) + len(sn_):
                          user_input.find('\r\n', user_input.find(sn_))]\
        .replace("(для Indiv и БТП)", "").strip()

    new_data['description_complane'] = desc_one.replace('(HE)', '').\
        replace('(Уточните, пожалуйста, в чем заключается неисправность)', '').strip() + " " + desc_two

    c_name = user_input[user_input.find(person_) + len(person_):
                        user_input.find('\r\n', (user_input.find(person_)))]
    new_data['client_name'] = c_name.strip()
    new_data['status_complane'] = 'NEW'
    new_data['additional_comment'] = '_'
    new_data['print_order'] = '0'
    new_data['price_status'] = 0
    new_data['transport_hours'] = 0

    return new_data


def parsing_from_input(user_input):
    """Takes data from user input textarea"""
    new_data = {}

    complaint_num = user_input[
                    user_input.find('Номер заявки') + 13:
                    user_input.find('от', user_input.find('Номер заявки'))
                    ]
    if user_input.find('Номер заявки') == -1:
        new_data['numer_complane'] = ''
    else:
        new_data['numer_complane'] = complaint_num.strip()

    new_data['account_id'] = 1

    complaint_date_start = user_input.find('от', user_input.find('Номер заявки')) + 3
    complaint_date = user_input[complaint_date_start: complaint_date_start + 10]  # Дата заявки
    new_data['date_creation'] = complaint_date
    new_data['date_complited_real'] = complaint_date

    c_files_user = str(user_input.find('Прикреплено файлов'))
    new_data['date_complited_fake'] = '1'
    if c_files_user == '-1':
        new_data['date_complited_fake'] = '0'

    complaint_phone = user_input[
                      user_input.find('Телефон') + 9:
                      user_input.find('\r\n', (user_input.find('Телефон')))
                      ]
    new_data['client_phone_num'] = complaint_phone

    c_address = user_input[user_input.find('Адрес:') + 9: user_input.find('\r\n', (user_input.find('Адрес:')))]
    c_address = str(input_address(c_address))  # Dadata address correction
    new_data['address_complane'] = c_address

    new_data['device_type'] = type_by_address(c_address)

    desc_one = user_input[user_input.find('Неисправность:') + 16: user_input.find('Описание проблемы пользователем:')]
    desc_two = user_input[user_input.find('Описание проблемы пользователем:') + 34:
                          user_input.find('Заключение сервисного')]
    temp_str = desc_one.strip() + ' ' + desc_two.strip()
    new_data['description_complane'] = temp_str.replace('(HE)', '')

    c_name = user_input[user_input.find('Контактное лицо:') + 17:
                        user_input.find('\r\n', (user_input.find('Контактное лицо:')))]
    new_data['client_name'] = c_name.strip()

    new_data['status_complane'] = 'NEW'
    new_data['additional_comment'] = '_'
    new_data['print_order'] = '0'
    new_data['price_status'] = 0
    new_data['transport_hours'] = 0

    return new_data


def hand_input_parsing(date_):
    """Takes data from user input textarea"""
    new_data = {'numer_complane': date_.get('hand_compl_num'),
                'account_id': 1,
                'date_creation': str(date.today()),
                'date_complited_real': str(date.today()),
                'date_complited_fake': '0',
                'client_phone_num': date_.get('phone')}

    tp = date_.get('phone')

    if len(tp) == 10:  # without +7 or 8 or 7 at begin
        new_data['client_phone_num'] = f'+7({tp[0:3]}){tp[3:6]}-{tp[6:10]}'
    if len(tp) == 11:  # 8 999 123 4567
        if tp[0] == '8':
            new_data['client_phone_num'] = f'+7({tp[1:4]}){tp[4:7]}-{tp[7:11]}'
        else:
            new_data['client_phone_num'] = f'+{tp[0]}({tp[1:4]}){tp[4:7]}-{tp[7:11]}'
    if len(tp) == 12:  # +7 999 123 4567
        new_data['client_phone_num'] = f'{tp[0:2]}({tp[2:5]}){tp[5:8]}-{tp[8:12]}'

    c_address = date_.get('address')
    c_address = str(input_address(c_address))  # Dadata address correction
    new_data['address_complane'] = c_address

    new_data['device_type'] = type_by_address(c_address)

    new_data['description_complane'] = date_.get('desription')
    new_data['client_name'] = date_.get('username')

    new_data['status_complane'] = 'NEW'
    new_data['additional_comment'] = '_'
    new_data['print_order'] = '0'
    new_data['price_status'] = 0
    new_data['transport_hours'] = 0

    return new_data


def input_address(c_address):
    """Dadata service for address correction"""
    dadata = Dadata(DADATA_TOKEN, DADATA_SECRET)

    try:
        result_address = dadata.clean("address", c_address)
    except:
        result_address = {'result': '~' + str(c_address)}

    return result_address['result']


def type_by_address(c_address):
    try:
        building_num = int(c_address[c_address.find(', д') + 3: c_address.find(' ', c_address.find(', д') + 4)])
    except ValueError as e:
        try:
            building_num = int(c_address[c_address.find(', д') + 3: c_address.find(',', c_address.find(', д') + 4)])
        except ValueError as e:
            try:
                building_num = int(c_address[c_address.find(', д') + 3: c_address.find('/', c_address.find(', д') + 4)])
            except ValueError as e:
                return 'Error'

    return type_by_address_func(c_address, building_num)


def type_by_address_func(c_address, building_num):
    visual_dev = ('Взлетная', 'Люберцы', 'Мисайлово', 'Зенино')

    if 'Самуила' in c_address:
        return '187F0001' if building_num % 2 == 0 else '187F000100'

    elif 'Бориса' in c_address:
        return '187F0001' if building_num <= 25 else '187F000100'

    elif 'Корнея' in c_address:
        return '187F0001' if building_num > 3 else '187F000100'

    elif 'Нововатутинский' in c_address:
        return '187F000100' if building_num == 14 else '187F0001'

    for item in visual_dev:
        if item in c_address:
            return '187F0002'

    return 'No_Address'
