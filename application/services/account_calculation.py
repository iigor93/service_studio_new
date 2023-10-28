from application.implemented import account_service
from application.services.num_to_tex_rus import num_to_text_rus
from application.app_config import AGREEMENT_NUM, Prices


def account_calculation(aid):
    account = account_service.get_one(aid)
    context = {}

    rub_1000 = []
    rub_1000_sum = 0
    rub_1000_order = 0

    rub_1500 = []
    rub_1500_sum = 0
    rub_1500_order = 0

    rub_diagnostic = []
    rub_diagnostic_sum = 0
    rub_diagnostic_hours = 0
    rub_diagnostic_order = 0

    rub_transport = []
    rub_transport_sum = 0
    rub_transport_hours = 0
    rub_transport_order = 0

    rub_sum = 0

    for item in account.complaint:
        if (item.device_type == '187F0001') or (item.device_type == '187F0002') or (item.device_type == '187F000100'):
            rub_1000.append(item.numer_complane)
            rub_1000_sum += int(str(item.price_status))

        elif item.device_type == '187F001400':
            rub_1500.append(item.numer_complane)
            rub_1500_sum += int(str(item.price_status))
            rub_1500_order = rub_1000_order + 1
        else:
            rub_diagnostic.append(item.numer_complane)
            rub_diagnostic_hours += int(str(item.price_status))

        if item.transport_hours > 0:
            rub_transport.append(item.numer_complane)
            rub_transport_hours += int(str(item.transport_hours))

    rub_counter = 0
    if rub_1000_sum > 0:
        rub_counter += 1
        rub_1000_order = rub_counter

    if rub_1500_sum > 0:
        rub_counter += 1
        rub_1500_order = rub_counter

    if rub_diagnostic_hours > 0:
        rub_counter += 1
        rub_diagnostic_order = rub_counter

    if rub_transport_hours > 0:
        rub_counter += 1
        rub_transport_order = rub_counter

    rub_diagnostic_sum = int(Prices.PRICE_DIAGNOSTIC * rub_diagnostic_hours)
    rub_transport_sum = int(rub_transport_hours * Prices.PRICE_TRANSPORT_ONE_HOUR)
    rub_sum = rub_1000_sum + rub_1500_sum + rub_diagnostic_sum + rub_transport_sum

    context['rub_1000'] = rub_1000
    context['rub_1000_sum'] = rub_1000_sum
    context['rub_1500'] = rub_1500
    context['rub_1500_sum'] = rub_1500_sum
    context['rub_diagnostic'] = rub_diagnostic
    context['rub_diagnostic_sum'] = rub_diagnostic_sum
    context['rub_diagnostic_hours'] = rub_diagnostic_hours
    context['rub_transport'] = rub_transport
    context['rub_transport_sum'] = rub_transport_sum
    context['rub_transport_hours'] = rub_transport_hours
    context['rub_sum'] = rub_sum
    context['rub_sum_text'] = num_to_text_rus(rub_sum)

    context['rub_1000_order'] = rub_1000_order
    context['rub_1500_order'] = rub_1500_order
    context['rub_diagnostic_order'] = rub_diagnostic_order
    context['rub_transport_order'] = rub_transport_order
    context['rub_counter'] = rub_counter
    context['account'] = account
    context['agreement'] = AGREEMENT_NUM.get('2023')

    return context
