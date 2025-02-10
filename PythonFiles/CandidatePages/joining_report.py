import datetime
import os
from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response
from Authentication.middleware import auth

joining_report_blueprint = Blueprint('joining_report', __name__)


def joining_report_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @joining_report_blueprint.route('/joining_report', methods=['GET', 'POST'])
    def joining_report():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        if session.get('report_uploaded'):
            # Redirect to the admin login page if the user is not logged in
            flash('Joining Report has been uploaded successfully', 'Success')

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """SELECT * FROM application_page WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchone()

        # print(records['joining_report'])

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
        return render_template('CandidatePages/joining_report.html', title="Joining Report", records=records,
                               user=user, photo=photo, finally_approved=finally_approved)

    @joining_report_blueprint.route('/joining_report_submit', methods=['GET', 'POST'])
    def joining_report_submit():
        email = session['email']
        print('Joining Email', email)
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """SELECT joining_report, joining_date, first_name, last_name FROM application_page WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchone()

        first_name = records['first_name']
        last_name = records['last_name']

        if request.method == 'POST':
            joining_report = save_file_joining_report(request.files['joining_report'], first_name, last_name)
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Fixed format for date
            current_time = datetime.datetime.now().strftime('%H:%M:%S')  # Fixed format for time

            # Handle case where joining_report is not already uploaded
            if not records.get('joining_report'):
                update_query = """UPDATE application_page 
                                      SET joining_report=%s, joining_report_uploaded_date=%s, joining_report_uploaded_time=%s 
                                      WHERE email = %s"""
                cursor.execute(update_query, (joining_report, current_date, current_time, email))
                cnx.commit()

                cursor.close()
                cnx.close()

                session['report_uploaded'] = True
                return redirect(url_for('joining_report.joining_report'))
            else:
                # Case where joining_report is already uploaded
                cursor.close()
                cnx.close()
                flash('Joining Report is Already Uploaded', 'Error')
                return "Joining report is already uploaded", 400
        else:
            cursor.close()
            cnx.close()
            return redirect(url_for('joining_report.joining_report'))  # Redirect for non-POST requests

    def save_file_joining_report(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['JOINING_REPORT'], filename))
            # return os.path.join(app.config['RENT_AGREEMENT_REPORT'], filename)
            return '/static/uploads/joining_reports/' + filename
        else:
            return "Save File"