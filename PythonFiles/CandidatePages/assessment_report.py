from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response
from authentication.middleware import auth
import os
import datetime

assessment_report_blueprint = Blueprint('assessment_report', __name__)


def assessment_report_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @assessment_report_blueprint.route('/assessment_report', methods=['GET', 'POST'])
    def assessment_report():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        if session.get('assessment'):
            # Redirect to the admin login page if the user is not logged in
            flash('Assessment Report has been uploaded successfully', 'success')

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
        return render_template('CandidatePages/assessment_report.html', title="Utilization Report", records=records,
                               user=user, photo=photo, finally_approved=finally_approved)

    @assessment_report_blueprint.route('/hra_utility_report_submit', methods=['GET', 'POST'])
    def hra_utility_report_submit():
        email = session['email']
        # print('Joining Email', email)
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """SELECT hra_utility_report, first_name, last_name FROM application_page WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchone()

        first_name = records['first_name']
        last_name = records['last_name']

        if request.method == 'POST':
            hra_utility_report = save_file_hra_utility_report(request.files['hra_utility_report'], first_name, last_name)
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Fixed format for date
            current_time = datetime.datetime.now().strftime('%H:%M:%S')  # Fixed format for time

            # Handle case where joining_report is not already uploaded
            if not records.get('hra_utility_report'):
                update_query = """UPDATE application_page 
                                          SET hra_utility_report=%s,
                                          hra_utility_uploaded_date=%s, hra_utility_uploaded_time=%s 
                                          WHERE email = %s
                                  """
                cursor.execute(update_query, (hra_utility_report, current_date, current_time, email))
                cnx.commit()

                cursor.close()
                cnx.close()

                session['assessment'] = True
                return redirect(url_for('assessment_report.assessment_report'))
            else:
                # Case where joining_report is already uploaded
                cursor.close()
                cnx.close()
                flash('Undertaking Report is Already Uploaded', 'Error')
                return "Undertaking report is already uploaded", 400
        else:
            cursor.close()
            cnx.close()
            return redirect(url_for('assessment_report.assessment_report'))  # Redirect for non-POST requests

    @assessment_report_blueprint.route('/fellowship_utility_report_submit', methods=['GET', 'POST'])
    def fellowship_utility_report_submit():
        email = session['email']
        # print('Joining Email', email)
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """SELECT fellowship_utility_report, first_name, last_name FROM application_page WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchone()

        first_name = records['first_name']
        last_name = records['last_name']

        if request.method == 'POST':
            fellowship_utility_report = save_file_fellowship_utility_report(request.files['fellowship_utility_report'], first_name, last_name)
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Fixed format for date
            current_time = datetime.datetime.now().strftime('%H:%M:%S')  # Fixed format for time

            # Handle case where joining_report is not already uploaded
            if not records.get('fellowship_utility_report'):
                update_query = """UPDATE application_page 
                                              SET fellowship_utility_report=%s,
                                              fellowship_utility_uploaded_date=%s, fellowship_utility_uploaded_time=%s 
                                              WHERE email = %s
                                      """
                cursor.execute(update_query, (fellowship_utility_report, current_date, current_time, email))
                cnx.commit()

                cursor.close()
                cnx.close()

                session['fellowship_assessment'] = True
                return redirect(url_for('assessment_report.assessment_report'))
            else:
                # Case where joining_report is already uploaded
                cursor.close()
                cnx.close()
                flash('Undertaking Report is Already Uploaded', 'Error')
                return "Undertaking report is already uploaded", 400
        else:
            cursor.close()
            cnx.close()
            return redirect(url_for('assessment_report.assessment_report'))  # Redirect for non-POST requests

    def save_file_hra_utility_report(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['HRA_UTILITY_REPORT'], filename))
            # return os.path.join(app.config['RENT_AGREEMENT_REPORT'], filename)
            return '/static/uploads/hra_utility_report/' + filename
        else:
            return "Save File"

    def save_file_fellowship_utility_report(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['FELLOWSHIP_UTILITY_REPORT'], filename))
            # return os.path.join(app.config['RENT_AGREEMENT_REPORT'], filename)
            return '/static/uploads/fellowship_utility_report/' + filename
        else:
            return "Save File"