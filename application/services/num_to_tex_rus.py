def num_to_text_rus(num):
    string = ['', '', '', '', '', '']
    num_to_text = list(str(num))

    if len(num_to_text) < 6:
        for i in (range(6 - len(num_to_text))):
            num_to_text.insert(0, 0)

    # единицы
    z = 5
    if num_to_text[z] == '1':
        string[z] = 'один'
    elif num_to_text[z] == '2':
        string[z] = 'два'
    elif num_to_text[z] == '3':
        string[z] = 'три'
    elif num_to_text[z] == '4':
        string[z] = 'четыре'
    elif num_to_text[z] == '5':
        string[z] = 'пять'
    elif num_to_text[z] == '6':
        string[z] = 'шесть'
    elif num_to_text[z] == '7':
        string[z] = 'семь'
    elif num_to_text[z] == '8':
        string[z] = 'восемь'
    elif num_to_text[z] == '9':
        string[z] = 'девять'

    # десятки
    z = 4
    if num_to_text[z] == '1':
        string[z] = ''

        if num_to_text[z + 1] == '1':
            string[z + 1] = 'одиннадцать'
        elif num_to_text[z + 1] == '2':
            string[z + 1] = 'двеннадцать'
        elif num_to_text[z + 1] == '3':
            string[z + 1] = 'тринадцать'
        elif num_to_text[z + 1] == '4':
            string[z + 1] = 'четырнадцать'
        elif num_to_text[z + 1] == '5':
            string[z + 1] = 'пятнадцать'
        elif num_to_text[z + 1] == '6':
            string[z + 1] = 'шестнадцать'
        elif num_to_text[z + 1] == '7':
            string[z + 1] = 'семнадцать'
        elif num_to_text[z + 1] == '8':
            string[z + 1] = 'восемнадцать'
        elif num_to_text[z + 1] == '9':
            string[z + 1] = 'девятнадцать'
        elif num_to_text[z + 1] == '0':
            string[z + 1] = 'десять'

    elif num_to_text[z] == '2':
        string[z] = 'двадцать'
    elif num_to_text[z] == '3':
        string[z] = 'тридцать'
    elif num_to_text[z] == '4':
        string[z] = 'сорок'
    elif num_to_text[z] == '5':
        string[z] = 'пятьдесят'
    elif num_to_text[z] == '6':
        string[z] = 'шестьдесят'
    elif num_to_text[z] == '7':
        string[z] = 'семьдесят'
    elif num_to_text[z] == '8':
        string[z] = 'восемьдесят'
    elif num_to_text[z] == '9':
        string[z] = 'девяносто'

    # сотни
    z = 3
    if num_to_text[z] == '1':
        string[z] = 'сто'
    elif num_to_text[z] == '2':
        string[z] = 'двести'
    elif num_to_text[z] == '3':
        string[z] = 'триста'
    elif num_to_text[z] == '4':
        string[z] = 'четыреста'
    elif num_to_text[z] == '5':
        string[z] = 'пятьсот'
    elif num_to_text[z] == '6':
        string[z] = 'шестьсот'
    elif num_to_text[z] == '7':
        string[z] = 'семьсот'
    elif num_to_text[z] == '8':
        string[z] = 'восемьсот'
    elif num_to_text[z] == '9':
        string[z] = 'девятьсот'

    # тысячи
    z = 2
    if num_to_text[z] == '1':
        string[z] = 'одна'
    elif num_to_text[z] == '2':
        string[z] = 'две'
    elif num_to_text[z] == '3':
        string[z] = 'три'
    elif num_to_text[z] == '4':
        string[z] = 'четыре'
    elif num_to_text[z] == '5':
        string[z] = 'пять'
    elif num_to_text[z] == '6':
        string[z] = 'шесть'
    elif num_to_text[z] == '7':
        string[z] = 'семь'
    elif num_to_text[z] == '8':
        string[z] = 'восемь'
    elif num_to_text[z] == '9':
        string[z] = 'девять'

    # десятки тысячи
    z = 1
    if num_to_text[z] == '1':
        string[z] = ''

        if num_to_text[z + 1] == '1':
            string[z + 1] = 'одиннадцать'
        elif num_to_text[z + 1] == '2':
            string[z + 1] = 'двеннадцать'
        elif num_to_text[z + 1] == '3':
            string[z + 1] = 'тринадцать'
        elif num_to_text[z + 1] == '4':
            string[z + 1] = 'четырнадцать'
        elif num_to_text[z + 1] == '5':
            string[z + 1] = 'пятнадцать'
        elif num_to_text[z + 1] == '6':
            string[z + 1] = 'шестнадцать'
        elif num_to_text[z + 1] == '7':
            string[z + 1] = 'семнадцать'
        elif num_to_text[z + 1] == '8':
            string[z + 1] = 'восемнадцать'
        elif num_to_text[z + 1] == '9':
            string[z + 1] = 'девятнадцать'
        elif num_to_text[z + 1] == '0':
            string[z + 1] = 'десять'

    elif num_to_text[z] == '2':
        string[z] = 'двадцать'
    elif num_to_text[z] == '3':
        string[z] = 'тридцать'
    elif num_to_text[z] == '4':
        string[z] = 'сорок'
    elif num_to_text[z] == '5':
        string[z] = 'пятьдесят'
    elif num_to_text[z] == '6':
        string[z] = 'шестьдесят'
    elif num_to_text[z] == '7':
        string[z] = 'семьдесят'
    elif num_to_text[z] == '8':
        string[z] = 'восемьдесят'
    elif num_to_text[z] == '9':
        string[z] = 'девяносто'

    # сотни тысяч
    z = 0
    if num_to_text[z] == '1':
        string[z] = 'сто'
    elif num_to_text[z] == '2':
        string[z] = 'двести'
    elif num_to_text[z] == '3':
        string[z] = 'триста'
    elif num_to_text[z] == '4':
        string[z] = 'четыреста'
    elif num_to_text[z] == '5':
        string[z] = 'пятьсот'
    elif num_to_text[z] == '6':
        string[z] = 'шестьсот'
    elif num_to_text[z] == '7':
        string[z] = 'семьсот'
    elif num_to_text[z] == '8':
        string[z] = 'восемьсот'
    elif num_to_text[z] == '9':
        string[z] = 'девятьсот'

    if string[0] != '' or string[1] != '' or string[2] != '':
        if string[2] == 'одна':
            string.insert(3, 'тысяча')
        elif string[2] == 'две' or string[2] == 'три' or string[2] == 'четыре':
            string.insert(3, 'тысячи')
        else:
            string.insert(3, 'тысяч')

    string_end = ''
    if string[-1] == 'один':
        string_end = ' рубль, 00 копеек'
    elif (string[-1] == 'два') or (string[-1] == 'три') or (string[-1] == 'четыре'):
        string_end = ' рубля, 00 копеек'
    else:
        string_end = ' рублей, 00 копеек'

    string = (' '.join(string)).strip()
    string = string.split()
    string_new = (' '.join(string) + string_end).strip().capitalize()
    # print(string_new)

    return string_new
