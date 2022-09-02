from application.implemented import complaint_service
from application.app_config import PRICE_DEFAULT


def compl_to_account(data_string, aid, from_account=False):
    if from_account:
        data_list = data_string
    else:
        data_list = data_string.strip().split('\r\n')

    all_complaints = {number: complaint_service.get_all_by_number(number) for number in data_list}
    good_complaints = []
    bad_complaints = []
    for key, value in all_complaints.items():
        if value != 'Not found':
            data = {'id': value.id, 'account_id': aid, 'price_status': PRICE_DEFAULT, 'status_complane': 'done'}
            complaint_service.update(data)
            good_complaints.append(key)
        else:
            bad_complaints.append(key)

    return f'Рекламации добавлены: {len(good_complaints)} шт, Рекламации не добавлены: {bad_complaints}'
