from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response
from authentication.middleware import auth
import datetime
import os

presenty_blueprint = Blueprint('presenty', __name__)


def presenty_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @presenty_blueprint.route('/presenty', methods=['GET', 'POST'])
    def presenty():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

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

        cursor.execute("""
                SELECT *
                FROM award_letter WHERE email = %s
            """, (email,))
        user_data = cursor.fetchone()

        print('User Data:', user_data['email'])

        if not user_data:
            cursor.close()
            cnx.close()
            return redirect('/login')

        joining_date = records.get('phd_registration_date')
        # reports = {f"monthly_report{i}": user_data.get(f"monthly_report{i}") for i in range(1, 61)}

        if joining_date:
            report_months = []
            start_dates = [joining_date + datetime.timedelta(days=i * 30) for i in range(60)]
            end_dates = [start_date + datetime.timedelta(days=30) for start_date in start_dates]
            zipped_dates = zip(start_dates, end_dates)

            start_month = joining_date.month
            current_month = start_month
            current_year = joining_date.year

            for i in range(60):
                report_months.append(current_month)
                current_month += 1
                if current_month > 12:
                    current_month = 1
                    current_year += 1

            zipped_dates = zip(start_dates, end_dates, report_months)
            print(f"Months for 60 Reports: {report_months}")
        else:
            zipped_dates = []
            report_months = []

        reports = {f"monthly_report{i}": user_data.get(f"monthly_report{i}") for i in range(1, 61)}
        dates = {f"submission_date_report{i}": user_data.get(f"submission_date_report{i}") for i in range(1, 61)}
        days = {f"submission_day_report{i}": user_data.get(f"submission_day_report{i}") for i in range(1, 61)}
        time = {f"submission_time_{i}": user_data.get(f"submission_time_{i}") for i in range(1, 61)}
        submitted_documents = [key for key, value in reports.items() if value]
        submitted_count = len(submitted_documents)

        # Debugging
        # print("Reports:", reports)
        # print("Dates:", dates)
        # print("Submitted Documents:", submitted_documents)

        return render_template('CandidatePages/presenty_report.html',
                               title="Presenty/Attendance Reports",
                               records=records,
                               user=user,
                               photo=photo,
                               finally_approved=finally_approved,
                               reports=reports,
                               submitted_count=submitted_count,
                               submitted_documents=submitted_documents,
                               zipped_dates=zipped_dates,
                               dates=dates,
                               days=days, time=time
                               )

    @presenty_blueprint.route('/submit_presenty', methods=['POST'])
    def submit_presenty():
        if 'email' not in session:
            return redirect('/login')

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute("SELECT first_name, last_name FROM application_page WHERE email = %s", (email,))
        result = cursor.fetchone()

        if not result:
            cursor.close()
            cnx.close()
            return redirect('/login')

        # Handle file uploads
        for i in range(1, 61):
            report = request.files.get(f'monthly_report{i}')
            if report:
                first_name = result['first_name']
                last_name = result['last_name']
                current_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Fixed format for date
                current_time = datetime.datetime.now().strftime('%H:%M:%S')  # Fixed format for date
                current_day = datetime.datetime.now().strftime('%A')  # Fixed format for time
                report_path = save_file_presenty_report(report, first_name, last_name)
                query = f"""
                UPDATE award_letter 
                SET 
                    monthly_report{i} = %s, 
                    submission_date_report{i} = %s, 
                    submission_time_{i} = %s, 
                    submission_day_report{i} = %s 
                WHERE email = %s
                """
                cursor.execute(query, (report_path, current_date, current_time, current_day, email))

        cnx.commit()
        cursor.close()
        cnx.close()

        return redirect(url_for('presenty.presenty'))

    def save_file_presenty_report(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['PRESENTY_REPORTS'], filename))
            # return os.path.join(app.config['PRESENTY_REPORTS'], filename)
            return '/static/uploads/presenty_reports/' + filename
        else:
            return "Save File"
