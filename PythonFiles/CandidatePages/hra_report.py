from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response
from authentication.middleware import auth
import datetime
import os

hra_report_blueprint = Blueprint('hra_report', __name__)


def hra_report_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @hra_report_blueprint.route('/hra_reports', methods=['GET'])
    def hra_reports():
        if 'email' not in session:
            # Redirect to the login page if the user is not logged in
            return redirect('/login')

        email = session['email']

        # Database connection
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """SELECT * FROM application_page WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchone()

        # Fetch user details in a single query
        cursor.execute("""
            SELECT first_name, last_name, phd_registration_date, rent_agreement1, rent_agreement2,
                   rent_agreement3, rent_agreement4, rent_agreement5, hostelier_report1, hostelier_report2,
                   hostelier_report3, hostelier_report4, hostelier_report5, hostelier1, hostelier2, hostelier3,
                   hostelier4, hostelier5
            FROM application_page WHERE email = %s
        """, (email,))
        user_data = cursor.fetchone()
        print(user_data)

        if not user_data:
            cursor.close()
            cnx.close()
            return redirect('/login')  # Redirect if no user data is found

        # Extract user information
        # reports = {
        #            f"rent_agreement{i}": user_data.get(f"rent_agreement{i}") for i in range(1, 6),
        #            f"hostelier_report{i}": user_data.get(f"hostelier_report{i}") for i in range(1, 6)
        #           }
        reports = {}
        for i in range(1, 6):
            reports[f"rent_agreement{i}"] = user_data[f"rent_agreement{i}"]  # Access directly
            reports[f"hostelier_report{i}"] = user_data[f"hostelier_report{i}"]  # Access directly
            reports[f"hostelier{i}"] = user_data[f"hostelier{i}"]  # Access directly

        joining_date = records.get('phd_registration_date')

        # Set user details and photo
        user = f"{records['first_name']} {records['last_name']}" if records else "Admin"
        photo = records['applicant_photo'] if records.get('applicant_photo') else '/static/assets/img/default_user.png'

        # Check fellowship approval status
        finally_approved = 'approved' if records.get('final_approval') == 'accepted' else 'pending'

        # Calculate submitted reports and dates
        submitted_documents = [key for key, value in reports.items() if value]
        print('Submitted Documents', submitted_documents)
        submitted_count = len(submitted_documents)
        print('Submitted Count', submitted_count)

        if joining_date:
            start_dates = [joining_date + datetime.timedelta(days=i * 365) for i in range(5)]
            end_dates = [start_date + datetime.timedelta(days=365) for start_date in start_dates]
        else:
            start_dates, end_dates = [], []

        # Close the database connection
        cursor.close()
        cnx.close()

        return render_template(
            'CandidatePages/hra_report.html',
            reports=reports,
            records=records,
            photo=photo,
            finally_approved=finally_approved,
            joining_date=joining_date,
            start_dates=start_dates,
            end_dates=end_dates,
            submitted_count=submitted_count,
            submitted_documents=submitted_documents,
            user=user,
            tite='HRA Reports'
        )

    @hra_report_blueprint.route('/submit_rent_agreement', methods=['POST'])
    def submit_rent_agreement():
        if 'email' not in session:
            # Redirect to the login page if the user is not logged in
            return redirect('/login')

        email = session['email']

        # Database connection
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        # Fetch user details to save the file with user's name
        cursor.execute("SELECT first_name, last_name FROM application_page WHERE email = %s", (email,))
        user_data = cursor.fetchone()

        if not user_data:
            cursor.close()
            cnx.close()
            return redirect(url_for('hra_report.hra_reports'))  # Redirect if no user data is found

        # Handle file uploads
        report_paths = []
        for i in range(1, 6):
            report = request.files.get(f'rent_agreement{i}')
            hostelier_report = request.files.get(f'hostelier_report{i}')
            hostelier = request.form.get(f'hostelier{i}')

            if report:
                # Save the uploaded report to a directory
                report_path = save_file_rent_agreement(report, user_data['first_name'], user_data['last_name'])
                report_paths.append((f'rent_agreement{i}', report_path))

            if hostelier_report:
                hostelier_report_path = save_file_rent_agreement(hostelier_report, user_data['first_name'],
                                                                 user_data['last_name'])
                report_paths.append((f'hostelier_report{i}', hostelier_report_path))

            if hostelier:
                report_paths.append((f'hostelier{i}', hostelier))

        # Update the database with the report paths
        for report_field, report_path in report_paths:
            cursor.execute(f"UPDATE application_page SET {report_field} = %s WHERE email = %s", (report_path, email))
        cnx.commit()

        # Close the database connection
        cursor.close()
        cnx.close()

        # Redirect back to the render route
        return redirect(url_for('hra_report.hra_reports'))

    def save_file_rent_agreement(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['RENT_AGREEMENT_REPORT'], filename))
            # return os.path.join(app.config['RENT_AGREEMENT_REPORT'], filename)
            return '/static/uploads/rent_agreement/' + filename
        else:
            return "Save File"