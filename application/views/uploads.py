import os
from datetime import date
from PIL import Image

from application.services.add_comp_to_account import compl_to_account
from application.services.pic_to_text import pic_to_text
from config import UPLOAD_FOLDER
from services.decorators import auth_required
from flask import Blueprint, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from application.implemented import complaint_service, account_service
from application.services.check_user import check_user


uploads = Blueprint('uploads', __name__, template_folder='templates', static_folder='static')


@uploads.route('/', methods=['GET', 'POST'], endpoint='upload_img')
@auth_required
def uploads_files():
    if request.method == 'POST':
        data_received = request.form.to_dict()

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.referrer)

        uploaded_files = request.files.getlist('file')
        files_uploaded = []
        complaints_dont_found = []
        complaints_without_ext = []
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            complaint_number_file = filename.split('.')[0]
            complaint = complaint_service.get_all_by_number(complaint_number_file)

            if 'HE' in complaint_number_file and complaint == 'Not found':
                """ Замена латинского HE на русское НЕ"""
                complaint_number_file = complaint_number_file.replace('HE', 'НЕ')
                complaint = complaint_service.get_all_by_number(complaint_number_file)

            if complaint == 'Not found':
                complaints_dont_found.append(f'{filename}')
                continue

            folder_year = f'{date.today().year}'
            folder_month = f'{date.today().month}'

            path = os.path.join(UPLOAD_FOLDER, folder_year)
            if not os.path.exists(path):
                os.mkdir(path)
            path = os.path.join(UPLOAD_FOLDER, folder_year, folder_month)
            if not os.path.exists(path):
                os.mkdir(path)

            file.save(os.path.join(UPLOAD_FOLDER, folder_year, folder_month, filename))
            new_date = {'filename': f'{folder_year}/{folder_month}/{filename}',
                        'id': complaint.id}
            complaint_service.update(new_date)
            files_uploaded.append(f'{filename}')
            complaints_without_ext.append(complaint_number_file)

        if data_received.get('id'):
            iid = data_received.get('id')
            flash(compl_to_account(complaints_without_ext, iid, from_account=True))

        flash(f'Files uploaded ({len(files_uploaded)}): {files_uploaded}')
        flash(f'Complaints doesnt exist({len(complaints_dont_found)}): {complaints_dont_found}')
        return redirect(request.referrer)


@uploads.route('/<year>/<month>/<filename>', methods=['GET', 'POST'], endpoint='get_img')
@auth_required
def download_file(filename, year, month):
    return send_from_directory(f'{UPLOAD_FOLDER}/{year}/{month}', filename)


@uploads.route('/tmp/<filename>', methods=['GET', 'POST'], endpoint='get_img_tmp')
@auth_required
def download_file_tmp(filename):
    return send_from_directory(f'{UPLOAD_FOLDER}/tmp/', filename)


@uploads.route('/upload_img_tmp', methods=['GET', 'POST'], endpoint='upload_img_tmp')
@auth_required
def uploads_files_tmp():
    """Загрузка файлов в папку tmp, распознавание текста"""
    if request.method == 'POST':
        data_received = request.form.to_dict()

        uploaded_files = request.files.getlist('file')

        folder_name = f'tmp'
        path = os.path.join(UPLOAD_FOLDER, folder_name)
        if not os.path.exists(path):
            os.mkdir(path)

        file_names = os.listdir(path)

        for file in file_names:
            """ remove all files from tmp folder """
            os.remove(os.path.join(path, file))

        for file in uploaded_files:
            """ save files from request """
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, folder_name, filename))

        file_names = pic_to_text(path)
        account_ = account_service.get_one(data_received.get('id'))

        data = {'filenames': file_names, 'account': account_}
        admin = check_user()
        if admin:
            data['admin'] = admin.get('role')
            data['user_name'] = admin.get('user_name')
        else:
            data['user_name'] = 'no_user'
            data['admin'] = 'no_admin'
        return render_template('account/account_pic_to_text.html', **data)


@uploads.route('/upload_tesseract', methods=['GET', 'POST'], endpoint='upload_tesseract')
@auth_required
def uploads_files_tesseract():
    """Привязка распознанных актов к рекламации и добавление к счету"""
    if request.method == 'POST':
        data_received = request.form.to_dict()
        print(data_received)
        uploaded_files = []

        folder_name = f'tmp'
        path_source = os.path.join(UPLOAD_FOLDER, folder_name)

        folder_year = f'{date.today().year}'
        folder_month = f'{date.today().month}'

        path_destination = os.path.join(UPLOAD_FOLDER, folder_year)
        if not os.path.exists(path_destination):
            os.mkdir(path_destination)
        path_destination = os.path.join(UPLOAD_FOLDER, folder_year, folder_month)
        if not os.path.exists(path_destination):
            os.mkdir(path_destination)

        account_ = account_service.get_one(data_received.get('id'))

        for file_name_ext, file_name_new in data_received.items():
            filename_old = file_name_ext
            if file_name_ext == 'id':
                continue
            if file_name_ext.split('.')[0] == file_name_new:
                filename_new = file_name_ext
            else:
                filename_new = file_name_new + '.' + file_name_ext.split('.')[1]
            uploaded_files.append(filename_new)
            os.replace(os.path.join(path_source, filename_old), os.path.join(path_destination, filename_new))

        files_uploaded = []
        complaints_dont_found = []
        complaints_without_ext = []
        for file in uploaded_files:
            filename = file
            complaint_number_file = filename.split('.')[0]
            complaint = complaint_service.get_all_by_number(complaint_number_file)

            if 'HE' in complaint_number_file and complaint == 'Not found':
                """ Замена латинского HE на русское НЕ"""
                complaint_number_file = complaint_number_file.replace('HE', 'НЕ')
                complaint = complaint_service.get_all_by_number(complaint_number_file)

            if complaint == 'Not found':
                complaints_dont_found.append(f'{filename}')
                continue

            new_date = {'filename': f'{folder_year}/{folder_month}/{filename}',
                        'id': complaint.id}
            complaint_service.update(new_date)
            files_uploaded.append(f'{filename}')
            complaints_without_ext.append(complaint_number_file)

        flash(compl_to_account(complaints_without_ext, account_.id, from_account=True))

        flash(f'Files uploaded ({len(files_uploaded)}): {files_uploaded}')
        flash(f'Complaints doesnt exist({len(complaints_dont_found)}): {complaints_dont_found}')

        return redirect(url_for('account.account_details', aid=account_.id))
