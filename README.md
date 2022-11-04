# service_studio_new

Сервис для регистрации и обработки сервисных заявок.
регистрация, обработка, закрытие заявки.
Выставление счетов.

Используется для собственных нужд

Flask, Docker, PostgreSQL

3.1.2 - Добавлена печать одного акта со страницы акта

3.1.3 - Remove "(HE)" from user description for new complaints

3.1.4 - Убрано "(НЕ)" при печати актов; добавлено checkbox для печати полностью пустого акта

3.2.0 - К модели complaint добавлено изображение. Множественная загрузка изображений, автопривязка по имени.

3.2.1 - Добавлено загрузка файлов со страницы счета, автопривязка рекламации к счету по названию файла.

3.2.2 - Добавлено отображение, что АВР загружен на странице счета.

3.2.3 - Сортировка заявок по часам выезда и названию.

3.2.4 - Добавлено "АА %COMPLAINT_NUMBER% AA" для распознавания номера.

3.2.5 - Добавление рекламаций из Bitrix24 (копирование текста)

3.2.6 - Добавление ручного ввода данных рекламации

3.2.7 - Замена русских и латинских символов в названии рекламации.

3.3.0 - Добавление фото рекламации к счету. Распознавание имени файла tesseract. Привязка сразу к счету.
        - Убран Bitrix по умолчанию.

3.3.1 - Порядок рекламаций "В работе" меняется перетаскиванием

3.3.2 - Обновление через отправку и получение JSON (Адрес и комментарий к заявке)

3.3.3 - Корректировка номера - единый формат +7 (ХХХ) ххх-хххх

3.3.4 - Добавлена фамилия в акты