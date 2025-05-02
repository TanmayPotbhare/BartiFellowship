from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response
from authentication.middleware import auth
import datetime
import os

halfyearly_blueprint = Blueprint('halfyearly', __name__)


def halfyearly_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @halfyearly_blueprint.route('/halfyearly', methods=['GET', 'POST'])
    def halfyearly():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        email = session.get('email')
        if not email:
            return redirect(url_for('login_signup.login'))  # Extra safety check

        submitted_documents = []

        # Database connection
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """SELECT * FROM application_page WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchone()

        # Fetch the saved reports for the user
        cursor.execute(
            f"SELECT half_yearly_report1, half_yearly_report2, half_yearly_report3, half_yearly_report4, half_yearly_report5, "
            f"half_yearly_report6, half_yearly_report7, half_yearly_report8, half_yearly_report9, half_yearly_report10 "
            f"FROM application_page WHERE email = %s",
            (email,))
        reports = cursor.fetchone()
        print(reports)
        # Count the number of submitted reports

        submitted_count = sum([1 for i in range(1, 11) if reports[f'half_yearly_report{i}']])
        for i in range(1, 11):
            if reports.get(f'half_yearly_report{i}'):
                submitted_documents.append(f'half_yearly_report{i}')

        if not records:
            cursor.close()
            cnx.close()
            return redirect(url_for('login_signup.login'))  # Redirect if no records are found

        # Set user details and photo
        user = f"{records['first_name']} {records['last_name']}" if records else "Admin"
        photo = records['applicant_photo'] if records.get('applicant_photo') else '/static/assets/img/default_user.png'

        # Check fellowship approval status
        finally_approved = 'approved' if records.get('final_approval') == 'accepted' else 'pending'

        # Submitted documents
        submitted_documents = [
            f'half_yearly_report{i}' for i in range(1, 11) if records.get(f'half_yearly_report{i}')
        ]
        submitted_count = len(submitted_documents)

        # Calculate start and end dates for reports
        joining_date = records.get('phd_registration_date')
        if joining_date:
            start_dates = [joining_date + datetime.timedelta(days=i * 30 * 6) for i in range(10)]
            end_dates = [start_date + datetime.timedelta(days=30 * 6) for start_date in start_dates]
        else:
            start_dates, end_dates = [], []

        report_months = []

        start_month = joining_date.month
        current_month = start_month
        current_year = joining_date.year

        for i in range(10):
            report_months.append(current_month)
            # Increment by 6 months
            current_month += 6
            if current_month > 12:
                years_to_add = (current_month - 1) // 12
                current_year += years_to_add
                current_month = (current_month - 1) % 12 + 1

        # Close the database connection
        cursor.close()
        cnx.close()

        # Render the template
        return render_template(
            'CandidatePages/halfyearly.html',
            title="Half Yearly Reports",
            records=records,
            reports=reports,
            user=user,
            photo=photo,
            finally_approved=finally_approved,
            submitted_count=submitted_count,
            submitted_documents=submitted_documents,
            start_dates=start_dates,
            end_dates=end_dates,
            report_months=report_months
        )

    @halfyearly_blueprint.route('/submit_half_yearly_reports', methods=['POST'])
    def submit_half_yearly_reports():
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
            return redirect(url_for('halfyearly.halfyearly'))  # Redirect to the rendering page if user not found

        report_paths = []
        for i in range(1, 11):
            report = request.files.get(f'half_yearly_report{i}')
            if report:
                first_name = result['first_name']
                last_name = result['last_name']
                # Save the uploaded report to a directory
                report_path = save_file_half_yearly(report, first_name, last_name)
                report_paths.append((f'half_yearly_report{i}', report_path))

        # Update the database with the report paths
        for report_field, report_path in report_paths:
            cursor.execute(f"UPDATE application_page SET {report_field} = %s WHERE email = %s", (report_path, email))
        cnx.commit()

        cursor.close()
        cnx.close()
        return redirect(url_for('halfyearly.halfyearly'))  # Redirect to the rendering page after submission

    def save_file_half_yearly(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['HALF_YEARLY_REPORTS'], filename))
            # return os.path.join(app.config['HALF_YEARLY_REPORTS'], filename)
            return '/static/uploads/half_yearly/' + filename
        else:
            return "Save File"