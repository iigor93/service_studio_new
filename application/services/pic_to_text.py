import os
import random
import re

import pytesseract
from PIL import Image


def pic_to_text(path):
    file_names = os.listdir(path)
    file_names_list = []

    for file in file_names:
        ext = file.split('.')[1]

        with Image.open(f'{path}/{file}') as image:
            w, h = image.size

            area = (w*0.05, 0, w*0.5, h*0.2)
            image = image.crop(area)
            # image.show()
            pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"
            string = pytesseract.image_to_string(image)

            string = string.replace(" ", "")
            start = string.find('AA')
            finish = string.find('AA', start + 1)

            if start == -1 and finish == -1:
                print('Text not found')
                file_names_list.append((f'{file}', f'crop_{file}'))
                image.save(f'{path}/crop_{file}')
            else:
                complaint_number = string[start + 2: finish].strip()
                regex = re.compile('[a-zA-Z]|[а-яА-Я]')
                complaint_number = regex.sub('', complaint_number)

                while complaint_number in file_names_list:
                    # print(file_names_list)
                    # print('string: ', string)
                    complaint_number = complaint_number + '_' + str(random.randint(0, 20))

                file_names_list.append((f'{complaint_number}.{ext}', f'{complaint_number}_crop.{ext}'))

                os.rename(f'{path}/{file}', f'{path}/{complaint_number}.{ext}')
                image.save(f'{path}/{complaint_number}_crop.{ext}')
    return file_names_list
