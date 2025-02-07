from Classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response
from Authentication.middleware import auth
import datetime
import os

upload_phd_blueprint = Blueprint('upload_phd', __name__)


def upload_phd_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @upload_phd_blueprint.route('/upload_phd', methods=['GET', 'POST'])
    def upload_phd():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        if session.get('phd_award'):
            # Redirect to the admin login page if the user is not logged in
            flash('PHD Certificate has been uploaded successfully', 'success')

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """SELECT * FROM application_page WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchone()

        # Check if the user is approved for fellowship no matter the year to show the desired sidebar.
        if records['final_approval'] == 'accepted':
            finally_approved = 'approved'
        else:
            finally_approved = 'pending'

        # Pass the user and Photo to the header and the template to render is neatly instead of keeping it in session.
        if records:
            user = records['first_name'] + ' ' + records['last_name']
            photo = records['applicant_photo']
        else:
            user = "Admin"
            photo = '/static/assets/img/default_user.png'
        return render_template('CandidatePages/upload_phd.html', title="Change Center Details", records=records,
                               user=user, photo=photo, finally_approved=finally_approved)

    @upload_phd_blueprint.route('/upload_phd_submit', methods=['GET', 'POST'])
    def upload_phd_submit():
        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """SELECT phd_award, first_name, last_name FROM application_page WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchone()

        first_name = records['first_name']
        last_name = records['last_name']

        if request.method == 'POST':
            phd_award = save_file_pdf_cert(request.files['phd_award'], first_name, last_name)
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Fixed format for date
            current_time = datetime.datetime.now().strftime('%H:%M:%S')  # Fixed format for time

            # Handle case where joining_report is not already uploaded

            update_query = """UPDATE application_page 
                                              SET phd_award=%s, 
                                              phd_award_uploaded_date=%s, phd_award_uploaded_time=%s 
                                              WHERE email = %s
                                      """
            cursor.execute(update_query,
                           (phd_award, current_date, current_time, email))
            cnx.commit()

            cursor.close()
            cnx.close()

            session['phd_award'] = True
            return redirect(url_for('upload_phd.upload_phd'))
        else:
            cursor.close()
            cnx.close()
            return redirect(url_for('upload_phd.upload_phd'))  # Redirect for non-POST requests

    def save_file_pdf_cert(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['PDF_CERTIFICATE'], filename))
            # return os.path.join(app.config['RENT_AGREEMENT_REPORT'], filename)
            return '/static/uploads/phd_certificate/' + filename
        else:
            return "Save File"
