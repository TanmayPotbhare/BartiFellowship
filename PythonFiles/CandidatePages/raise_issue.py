import bcrypt
from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response
from authentication.middleware import auth
import os
import random
import string
from datetime import datetime

raise_issue_blueprint = Blueprint('raise_issue', __name__)


def raise_issue_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @raise_issue_blueprint.route('/raise_issue', methods=['GET', 'POST'])
    def raise_issue():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """SELECT * FROM issue_raised WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchall()
        # print(records)

        sql2 = """SELECT * FROM application_page WHERE email = %s"""
        cursor.execute(sql2, (email,))
        application_records = cursor.fetchall()

        # Pass the user and Photo to the header and the template to render is neatly instead of keeping it in session.
        if application_records:
            user = application_records[0]['first_name'] + ' ' + application_records[0]['last_name']
            photo = application_records[0]['applicant_photo']
        else:
            user = "Admin"
            photo = '/static/assets/img/default_user.png'

        return render_template('CandidatePages/raise_issue.html', title="Raise Issue", records=records,application_records=application_records,
                               user=user, photo=photo)



    @raise_issue_blueprint.route('/submit_raise_issue', methods=['GET', 'POST'])
    def submit_raise_issue():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """SELECT * FROM application_page WHERE email = %s"""
        cursor.execute(sql, (email,))
        application_records = cursor.fetchall()

        if application_records:
            print(application_records)
            candidate_fullname = application_records[0]['first_name'] + application_records[0]['middle_name'] + application_records[0]['last_name']
            first_name = application_records[0]['first_name']
            last_name = application_records[0]['last_name']

        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d") 
        current_time = now.strftime("%H:%M:%S") 

        if request.method == 'POST':
            ticket = generate_ticket_id()
            email = session['email']
            issue_subject = request.form['issue_subject']
            description = request.form['description']
            photo = request.files['document']
            fullname = candidate_fullname
            date = current_date
            time = current_time 
            status = "pending"

            # Handle file upload (applicant's photo)
            document_path = save_applicant_photo(photo, first_name, last_name)

            # Save the form data to the database
            sql = """
            INSERT INTO issue_raised (
                ticket, email, issue_subject, description, document, fullname, date, time, status
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """
            values = (
                ticket, email, issue_subject, description, document_path, fullname, date, time, status
            )

            cursor.execute(sql, values)
            cnx.commit()
            flash('Your issue is reported Successfully.', 'success')
            return redirect(url_for('raise_issue.raise_issue'))
        else:
            return redirect(url_for('raise_issue.raise_issue'))

    def save_applicant_photo(photo, firstname, lastname):
        if photo:
            filename = f"{firstname}_{lastname}_{photo.filename}"
            photo.save(os.path.join(app.config['UPLOAD_PHOTO_SECTION1'], filename))
            # return os.path.join(app.config['UPLOAD_PHOTO_SECTION1'], filename)
            return '/static/uploads/image_retrive/' + filename
        else:
            return "Save File"

    def generate_ticket_id():
        """Generates a random 4-digit ticket ID with a '#' prefix."""
        digits = ''.join(random.choices(string.digits, k=4))
        return f"#{digits}"