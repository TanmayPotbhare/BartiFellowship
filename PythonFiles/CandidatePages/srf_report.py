from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response
from authentication.middleware import auth
import datetime
import os

srf_report_blueprint = Blueprint('srf_report', __name__)

def srf_report_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @srf_report_blueprint.route('/srf_report', methods=['GET', 'POST'])
    def srf_report():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))
        email = session['email']
        if session.get('srf'):
            # Redirect to the admin login page if the user is not logged in
            # flash('srf Report has been uploaded successfully', 'Success')

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
        return render_template('CandidatePages/srf_report.html', title="SRF Report", records=records,
                               doc_records = doc_records, user=user, photo=photo, finally_approved=finally_approved)

    @srf_report_blueprint.route('/upgradation_report_submit', methods=['GET', 'POST'])
    def upgradation_report_submit():
        email = session['email']
        print('SRF Email', email)
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

        sql = """SELECT upgradation_doc FROM documents WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchone()

        if request.method == 'POST':
            upgradation_doc = save_file_upgradation_report(request.files['srf_doc'], first_name, last_name)
            # srf_doc_date = request.form['srf_doc_date']
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Fixed format for date
            current_time = datetime.datetime.now().strftime('%H:%M:%S')  # Fixed format for time

            if document_record:
                # UPDATE existing document
                update_query = """
                    UPDATE documents 
                    SET upgradation_doc = %s, upgradation_doc_uploaded_date = %s, upgradation_doc_uploaded_time = %s 
                    WHERE email = %s
                """
                cursor.execute(update_query, (upgradation_doc, current_date, current_time, email))
                flash('SRF Report updated successfully.', 'Success')
            else:
                # INSERT new document
                insert_query = """
                    INSERT INTO documents 
                    (applicant_id_fk, email, upgradation_doc, upgradation_doc_uploaded_date, upgradation_doc_uploaded_time) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (applicant_id, email, upgradation_doc, current_date, current_time))
                flash('SRF Report uploaded successfully.', 'Success')

            cnx.commit()
            cursor.close()
            cnx.close()

            session['srf'] = True
            flash('Upgradation Report submitted successfully', 'success')
            return redirect(url_for('srf_report.srf_report'))
    
        else:
            cursor.close()
            cnx.close()
            return redirect(url_for('srf_report.srf_report'))  # Redirect for non-POST requests

    def save_file_upgradation_report(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['UPGRADATION_REPORT'], filename))
            # return os.path.join(app.config['RENT_AGREEMENT_REPORT'], filename)
            return '/static/uploads/upgradation_doc/' + filename
        else:
            return "Save File"
        

    @srf_report_blueprint.route('/three_member_committee_report_submit', methods=['GET', 'POST'])
    def three_member_committee_report_submit():
        email = session['email']
        print('Three Member Committee Email', email)
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

        sql = """SELECT three_member_committee_doc FROM documents WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchone()

        if request.method == 'POST':
            three_member_committee_doc = save_file_three_member_committee_report(request.files['three_member_committee_doc'], first_name, last_name)
            # three_member_committee_doc_date = request.form['three_member_doc_date']
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Fixed format for date
            current_time = datetime.datetime.now().strftime('%H:%M:%S')  # Fixed format for time

            if document_record:
                # UPDATE existing document
                update_query = """
                    UPDATE documents 
                    SET three_member_committee_doc = %s, three_member_doc_uploaded_date = %s, three_member_doc_uploaded_time = %s 
                    WHERE email = %s
                """
                cursor.execute(update_query, (three_member_committee_doc, current_date, current_time, email))
                flash('Three member committee Report updated successfully.', 'Success')
            else:
                # INSERT new document
                insert_query = """
                    INSERT INTO documents 
                    (applicant_id_fk, email, three_member_committee_doc, three_member_doc_uploaded_date, three_member_doc_uploaded_time) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (applicant_id, email, three_member_committee_doc, current_date, current_time))
                flash('Three member committee Report uploaded successfully.', 'Success')

            cnx.commit()
            cursor.close()
            cnx.close()

            session['three_member_committee'] = True
            flash('Three member committee Report submitted successfully', 'success')
            return redirect(url_for('srf_report.srf_report'))
    
        else:
            cursor.close()
            cnx.close()
            return redirect(url_for('srf_report.srf_report'))  # Redirect for non-POST requests

    def save_file_three_member_committee_report(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['THREE_MEMBER_COMMITTEE_REPORT'], filename))
            return '/static/uploads/three_member_committee_doc/' + filename
        else:
            return "Save File"