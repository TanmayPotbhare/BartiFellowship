from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response
from authentication.middleware import auth
from datetime import datetime

withdraw_fellowship_blueprint = Blueprint('withdraw_fellowship', __name__)


def withdraw_fellowship_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @withdraw_fellowship_blueprint.route('/withdraw_fellowship', methods=['GET', 'POST'])
    def withdraw_fellowship():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        if request.method == 'POST':
            # Handle form submission (withdrawal request)
            try:
                current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get current date and time
                current_time = datetime.now().strftime('%H:%M:%S')  # Get current time

                sql_update = """
                    UPDATE signup
                    SET fellowship_withdrawn = 'withdrawn',
                        request_withdrawal = 1,
                        withdrawal_request_date = %s,
                        withdrawal_request_time = %s
                    WHERE email = %s
                """
                cursor.execute(sql_update, (current_date, current_time, email))
                cnx.commit()
                cursor.close()
                cnx.close()

                # Fetch records again to populate the sidebar and header
                cnx, cursor = connect_param.connect(use_dict=True) # Reconnect
                sql = """SELECT * FROM application_page WHERE email = %s"""
                cursor.execute(sql, (email,))
                records = cursor.fetchall()

                if records and records[0]['final_approval'] == 'accepted':
                    finally_approved = 'approved'
                else:
                    finally_approved = 'pending'

                if records:
                    user = records[0]['first_name'] + ' ' + records[0]['last_name']
                    photo = records[0]['applicant_photo']
                else:
                    user = "Admin"
                    photo = '/static/assets/img/default_user.png'

                flash("You request is successfully submitted.", "success")    

                return render_template('CandidatePages/withdraw_fellowship.html', title="Withdraw Fellowship", 
                                       records=records, user=user, photo=photo, finally_approved=finally_approved)
    
            except Exception as e:
                cursor.close()
                cnx.close()
                # Fetch records again to populate the sidebar and header
            cnx, cursor = connect_param.connect(use_dict=True) # Reconnect
            sql = """SELECT * FROM application_page WHERE email = %s"""
            cursor.execute(sql, (email,))
            records = cursor.fetchall()

            if records and records[0]['final_approval'] == 'accepted':
                finally_approved = 'approved'
            else:
                finally_approved = 'pending'

            if records:
                user = records[0]['first_name'] + ' ' + records[0]['last_name']
                photo = records[0]['applicant_photo']
            else:
                user = "Admin"
                photo = '/static/assets/img/default_user.png'

                flash(f"Error while submitting the Request: {e}", "error")
            return render_template('CandidatePages/withdraw_fellowship.html', title="Withdraw Fellowship",
                                   records=records, user=user, photo=photo, finally_approved=finally_approved)

        else:
            # Handle GET requests (initial page load)
            sql = """SELECT * FROM application_page WHERE email = %s"""
            cursor.execute(sql, (email,))
            records = cursor.fetchall()


            # The "finally_approved" status is used in the sidebar to display the options conditionally 
            if records and records[0]['final_approval'] == 'accepted':
                finally_approved = 'approved'
            else:
                finally_approved = 'pending'

            # The "user" and "photo" is used in the header to display the Candidate's Profile
            if records:
                user = records[0]['first_name'] + ' ' + records[0]['last_name']
                photo = records[0]['applicant_photo']
            else:
                user = "Admin"
                photo = '/static/assets/img/default_user.png'

            return render_template('CandidatePages/withdraw_fellowship.html', title="Withdraw Fellowship", records=records,
                                user=user, photo=photo, finally_approved=finally_approved)