from dadata import Dadata
from config import DADATA_TOKEN, DADATA_SECRET


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
