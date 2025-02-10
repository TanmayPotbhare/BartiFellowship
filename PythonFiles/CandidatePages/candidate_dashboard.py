from Classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response
from Authentication.middleware import auth

candidate_dashboard_blueprint = Blueprint('candidate_dashboard', __name__)


def candidate_dashboard_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @candidate_dashboard_blueprint.route('/candidate_dashboard')
    def candidate_dashboard():
        """
            This function is used to display the records of users after logging in. This is the first page
            which is shown to the user and consists of conditioning of sidebar according to the status of fellowship.
        """
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))
        else:
            if session.get('show_login_flash', True):  # Retrieve and clear the flag
                flash('Successfully Logged in to Candidate Dashboard', 'success')
                # set the flag to "False" to prevent the flash message from being diaplayed repetitively displayed
                session['show_login_flash'] = False

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """SELECT * FROM application_page WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchall()

        # Check if the user is approved for fellowship no matter the year to show the desired sidebar.
        if records[0]['final_approval'] == 'accepted':
            finally_approved = 'approved'
        else:
            finally_approved = 'pending'

        # Pass the user and Photo to the header and the template to render is neatly instead of keeping it in session.
        if records:
            user = records[0]['first_name'] + ' ' + records[0]['last_name']
            photo = records[0]['applicant_photo']
        else:
            user = "Admin"
            photo = '/static/assets/img/default_user.png'

        # Convert the Date to standard Format
        first_record = records[0]
        DoB = first_record['date_of_birth'] # Date of Birth
        formatted_date_of_birth = DoB.strftime('%d-%b-%Y')   
 
        application_date = first_record['application_date'] # Application Date
        formatted_application_date = application_date.strftime('%d-%b-%Y')

        PHD_reg_date = first_record['phd_registration_date'] # PHD Registration Date
        formatted_PHD_reg_date = PHD_reg_date.strftime('%d-%b-%Y')

        return render_template('CandidatePages/candidate_dashboard.html', title="My Profile", records=records,
                               user=user, photo=photo, finally_approved=finally_approved, 
                               formatted_date_of_birth=formatted_date_of_birth,
                               formatted_application_date=formatted_application_date,
                               formatted_PHD_reg_date=formatted_PHD_reg_date)

    @candidate_dashboard_blueprint.route('/adhaar_seeding')
    def adhaar_seeding():

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """SELECT * FROM application_page WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchall()

        # Check if the user is approved for fellowship no matter the year to show the desired sidebar.
        if records[0]['final_approval'] == 'accepted':
            finally_approved = 'approved'
        else:
            finally_approved = 'pending'

        if records:
            user = records[0]['first_name'] + ' ' + records[0]['last_name']
            photo = records[0]['applicant_photo']
        else:
            user = "Admin"
            photo = '/static/assets/img/default_user.png'
        return render_template('CandidatePages/adhaar_seeding.html', title="Aadhaar Seeding", records=records,
                               user=user, photo=photo, finally_approved=finally_approved)