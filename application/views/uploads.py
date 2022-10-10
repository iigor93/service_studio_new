import os
from datetime import date

from application.services.add_comp_to_account import compl_to_account
from config import UPLOAD_FOLDER
from services.decorators import auth_required
from flask import Blueprint, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from application.implemented import complaint_service


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
