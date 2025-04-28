from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response
from authentication.middleware import auth
import os
import datetime

utilization_report_blueprint = Blueprint('utilization_report', __name__)


def utilization_report_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @utilization_report_blueprint.route('/utilization_report', methods=['GET', 'POST'])
    def utilization_report():
        if not session.get('logged_in_from_login'):
            return redirect(url_for('login_signup.login'))

        email = session.get('email')
        if not email:
            return redirect(url_for('login_signup.login'))

        hra_submitted_documents = []
        hra_reports = {}
        fellowship_submitted_documents = []
        fellowship_reports = {} # Initialize an empty dictionary to hold all reports

        # Database connection
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql_app_page = """SELECT hra_utility_report, fellowship_utility_report,
                        first_name, middle_name, last_name, applicant_photo, final_approval
                        FROM application_page WHERE email = %s"""
        cursor.execute(sql_app_page, (email,))
        app_page_record = cursor.fetchone()
        if not app_page_record:
            cursor.close()
            cnx.close()
            return redirect(url_for('login_signup.login'))

        # Fetch HRA Reports
        if app_page_record.get('hra_utility_report'):
            hra_reports['hra_utility_doc1'] = app_page_record['hra_utility_report']
            hra_submitted_documents.append('hra_utility_doc1')

        hra_doc_fields = ["hra_utility_doc2", "hra_utility_doc3", "hra_utility_doc4", "hra_utility_doc5"]
        sql_hra_docs = f"""SELECT {', '.join(hra_doc_fields)}
                        FROM documents WHERE email = %s AND hra_utility_doc2 IS NOT NULL OR hra_utility_doc3 IS NOT NULL OR hra_utility_doc4 IS NOT NULL OR hra_utility_doc5 IS NOT NULL"""
        cursor.execute(sql_hra_docs, (email,))
        hra_doc_records = cursor.fetchone()

        if hra_doc_records:
            for i, field in enumerate(hra_doc_fields):
                if hra_doc_records.get(field):
                    hra_reports[f'hra_utility_doc{i + 2}'] = hra_doc_records[field]
                    hra_submitted_documents.append(f'hra_utility_doc{i + 2}')

        hra_submitted_count = len(hra_submitted_documents)

        # Fetch Fellowship/Contingency Reports
        if app_page_record.get('fellowship_utility_report'):
            fellowship_reports['fellowship_utility_doc1'] = app_page_record['fellowship_utility_report']
            fellowship_submitted_documents.append('fellowship_utility_doc1')

        fellowship_doc_fields = ["fellowship_utility_doc2", "fellowship_utility_doc3", "fellowship_utility_doc4", "fellowship_utility_doc5"]
        sql_fellowship_docs = f"""SELECT {', '.join(fellowship_doc_fields)}
                                FROM documents WHERE email = %s AND fellowship_utility_doc2 IS NOT NULL OR fellowship_utility_doc3 IS NOT NULL OR fellowship_utility_doc4 IS NOT NULL OR fellowship_utility_doc5 IS NOT NULL"""
        cursor.execute(sql_fellowship_docs, (email,))
        fellowship_doc_records = cursor.fetchone()

        if fellowship_doc_records:
            for i, field in enumerate(fellowship_doc_fields):
                if fellowship_doc_records.get(field):
                    fellowship_reports[f'fellowship_utility_doc{i + 2}'] = fellowship_doc_records[field]
                    fellowship_submitted_documents.append(f'fellowship_utility_doc{i + 2}')

        fellowship_submitted_count = len(fellowship_submitted_documents)

        # Set user details and photo
        user = f"{app_page_record['first_name']} {app_page_record['last_name']}"
        photo = app_page_record['applicant_photo'] if app_page_record.get('applicant_photo') else '/static/assets/img/default_user.png'

        # Check fellowship approval status
        finally_approved = 'approved' if app_page_record.get('final_approval') == 'accepted' else 'pending'

        # Close the database connection
        cursor.close()
        cnx.close()

        return render_template(
            'CandidatePages/utilization_report.html',
            title="HRA & Contingency Utilization Reports",
            records=app_page_record,
            hra_reports=hra_reports,
            hra_submitted_count=hra_submitted_count,
            hra_submitted_documents=hra_submitted_documents,
            fellowship_reports=fellowship_reports,
            fellowship_submitted_count=fellowship_submitted_count,
            fellowship_submitted_documents=fellowship_submitted_documents,
            user=user,
            photo=photo,
            finally_approved=finally_approved,
        )

    @utilization_report_blueprint.route('/hra_utility_report_submit', methods=['GET', 'POST'])
    def hra_utility_report_submit():
        if 'email' not in session:
            return redirect('/login')

        email = session['email']

        # Database connection
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        # Fetch user details
        cursor.execute("SELECT first_name, last_name FROM application_page WHERE email = %s", (email,))
        result = cursor.fetchone()

        if not result:
            return redirect(url_for('utilization_report.utilization_report'))

        first_name = result['first_name']
        last_name = result['last_name']
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.datetime.now().strftime('%H:%M:%S')

        # Handle the first HRA report (updates application_page)
        report1 = request.files.get('hra_utility_report1')
        if report1:
            report_path = save_file_hra_utility_report(report1, first_name, last_name)
            cursor.execute(
                "UPDATE application_page SET hra_utility_report = %s, "
                "hra_utility_uploaded_date = %s, hra_utility_uploaded_time = %s "
                "WHERE email = %s",
                (report_path, current_date, current_time, email)
            )
            cnx.commit()

        # Handle subsequent HRA reports (inserts/updates documents table)
        for i in range(2, 6):
            report = request.files.get(f'hra_utility_report{i}')
            if report:
                report_path = save_file_hra_utility_report(report, first_name, last_name)
                doc_field = f'hra_utility_doc{i}'
                date_field = f'hra_utility_uploaded_date{i}'
                time_field = f'hra_utility_uploaded_time{i}'

                cursor.execute("SELECT email FROM documents WHERE email = %s", (email,))
                existing_record = cursor.fetchone()

                if existing_record:
                    sql_update_doc = f"""UPDATE documents SET {doc_field} = %s, {date_field} = %s, {time_field} = %s
                                        WHERE email = %s"""
                    cursor.execute(sql_update_doc, (report_path, current_date, current_time, email))
                else:
                    sql_insert_doc = f"""INSERT INTO documents (email, {doc_field}, {date_field}, {time_field})
                                        VALUES (%s, 'hra_utility_report', %s, %s, %s)"""
                    cursor.execute(sql_insert_doc, (email, report_path, current_date, current_time))
                cnx.commit()

        cursor.close()
        cnx.close()
        return redirect(url_for('utilization_report.utilization_report'))

    def save_file_hra_utility_report(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['HRA_UTILITY_REPORT'], filename))
            return '/static/uploads/hra_utility_report/' + filename
        else:
            return None # Changed to None for consistency

    @utilization_report_blueprint.route('/fellowship_utility_report_submit', methods=['POST'])
    def fellowship_utility_report_submit():
        if 'email' not in session:
            return redirect('/login')

        email = session['email']

        # Database connection
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        # Fetch user details
        cursor.execute("SELECT first_name, last_name FROM application_page WHERE email = %s", (email,))
        result = cursor.fetchone()

        if not result:
            return redirect(url_for('utilization_report.utilization_report'))

        first_name = result['first_name']
        last_name = result['last_name']
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.datetime.now().strftime('%H:%M:%S')

        # Handle the first Fellowship/Contingency report (updates application_page)
        report1 = request.files.get('fellowship_utility_report1')
        if report1:
            report_path = save_file_fellowship_utility_report(report1, first_name, last_name)
            cursor.execute(
                "UPDATE application_page SET fellowship_utility_report = %s, "
                "fellowship_utility_uploaded_date = %s, fellowship_utility_uploaded_time = %s "
                "WHERE email = %s",
                (report_path, current_date, current_time, email)
            )
            cnx.commit()

        # Handle subsequent Fellowship/Contingency reports (inserts/updates documents table)
        for i in range(2, 6):
            report = request.files.get(f'fellowship_utility_report{i}')
            if report:
                report_path = save_file_fellowship_utility_report(report, first_name, last_name)
                doc_field = f'fellowship_utility_doc{i}'
                date_field = f'fellowship_utility_uploaded_date{i}'
                time_field = f'fellowship_utility_uploaded_time{i}'

                cursor.execute("SELECT email FROM documents WHERE email = %s", (email,))
                existing_record = cursor.fetchone()

                if existing_record:
                    sql_update_doc = f"""UPDATE documents SET {doc_field} = %s, {date_field} = %s, {time_field} = %s
                                        WHERE email = %s """
                    cursor.execute(sql_update_doc, (report_path, current_date, current_time, email))
                else:
                    sql_insert_doc = f"""INSERT INTO documents (email, {doc_field}, {date_field}, {time_field})
                                        VALUES (%s, 'fellowship_utility_report', %s, %s, %s)"""
                    cursor.execute(sql_insert_doc, (email, report_path, current_date, current_time))
                cnx.commit()

        cursor.close()
        cnx.close()
        return redirect(url_for('utilization_report.utilization_report'))

    def save_file_fellowship_utility_report(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['FELLOWSHIP_UTILITY_REPORT'], filename))
            return '/static/uploads/fellowship_utility_report/' + filename
        else:
            return None