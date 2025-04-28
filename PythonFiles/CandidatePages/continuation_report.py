from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response
from authentication.middleware import auth
import datetime
import os


continuation_report_blueprint = Blueprint('continuation_report', __name__)


def continuation_report_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @continuation_report_blueprint.route('/continuation_report', methods=['GET', 'POST'])
    def continuation_report():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))
        email = session['email']
        if session.get('continuation'):
            # Redirect to the admin login page if the user is not logged in
            # flash('Continuation Report has been uploaded successfully', 'success')

            email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """SELECT * FROM application_page WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchone()

        sql = """SELECT * FROM documents WHERE email = %s"""
        cursor.execute(sql, (email,))
        doc_records = cursor.fetchone()

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
        return render_template('CandidatePages/continuation_report.html', title="Continuation Report", records=records,
                               user=user, photo=photo, doc_records=doc_records, finally_approved=finally_approved)

    @continuation_report_blueprint.route('/continuation_report_submit', methods=['GET', 'POST'])
    def continuation_report_submit():
        email = session['email']
        print('Continuation Email', email)
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)
        
        # Fetch first_name, last_name, and applicant_id from application_page
        sql = """SELECT applicant_id, first_name, last_name FROM application_page WHERE email = %s"""
        cursor.execute(sql, (email,))
        application_data = cursor.fetchone()

        if not application_data:
            flash('Application data not found.', 'Error')
            cursor.close()
            cnx.close()
            return "Application data not found", 400

        applicant_id = application_data['applicant_id']
        first_name = application_data['first_name']
        last_name = application_data['last_name']

        # Check if record exists in documents table
        sql = """SELECT doc_id FROM documents WHERE email = %s"""
        cursor.execute(sql, (email,))
        document_record = cursor.fetchone()

        sql = """SELECT continuation_doc, continuation_doc_date FROM documents WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchone()

        if request.method == 'POST':
            continuation_doc = save_file_continuation_report(request.files['continuation_doc'], first_name, last_name)
            continuation_doc_date = request.form['continuation_doc_date']
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Fixed format for date
            current_time = datetime.datetime.now().strftime('%H:%M:%S')  # Fixed format for time

            if document_record:
                # UPDATE existing document
                update_query = """
                    UPDATE documents 
                    SET continuation_doc = %s, continuation_doc_date = %s, 
                        continuation_doc_uploaded_date = %s, continuation_doc_uploaded_time = %s 
                    WHERE email = %s
                """
                cursor.execute(update_query, (continuation_doc, continuation_doc_date, current_date, current_time, email))
                flash('Continuation Report updated successfully.', 'Success')
            else:
                # INSERT new document
                insert_query = """
                    INSERT INTO documents 
                    (applicant_id_fk, email, continuation_doc, continuation_doc_date, continuation_doc_uploaded_date, continuation_doc_uploaded_time) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (applicant_id, email, continuation_doc, continuation_doc_date, current_date, current_time))
                flash('Continuation Report uploaded successfully.', 'Success')

            cnx.commit()
            cursor.close()
            cnx.close()

            session['continuation'] = True
            flash('Continuation Report submitted successfully', 'success')
            return redirect(url_for('continuation_report.continuation_report'))
    
        else:
            cursor.close()
            cnx.close()
            return redirect(url_for('continuation_report.continuation_report'))  # Redirect for non-POST requests

    def save_file_continuation_report(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['CONTINUATION_REPORT'], filename))
            # return os.path.join(app.config['RENT_AGREEMENT_REPORT'], filename)
            return '/static/uploads/continuation_doc/' + filename
        else:
            return "Save File"