from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response
from authentication.middleware import auth
import datetime
import os

installments_blueprint = Blueprint('installments', __name__)


def installments_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @installments_blueprint.route('/installments')
    def installments():
        email = session['email']

        # Database connection
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        # Fetch user details
        cursor.execute("SELECT * FROM signup WHERE email=%s", (email,))
        signup_year = cursor.fetchone()

        sign_year = signup_year['year']

        # Fetch user details
        cursor.execute("SELECT * FROM application_page WHERE email=%s", (email,))
        records = cursor.fetchone()

        if records:
            year = records['phd_registration_year']
            startDate = records['final_approved_date']
        else:
            year = None
            startDate = None  # Initialize startDate to avoid further issues

        # Fetch installment and payment details
        cursor.execute("SELECT * FROM installments WHERE email=%s", (email,))
        installments = cursor.fetchall()

        cursor.execute(f"SELECT * FROM payment_sheet_{sign_year} WHERE email=%s", (email,))
        record = cursor.fetchall()

        # Assuming only one row in record
        today = datetime.datetime.today()
        installment_list = []  # Initialize the list here
        total_period = 0  # Initialize total_period
        total_balance = 0  # Initialize total_balance

        if record:  # Only proceed if record is not empty
            for row in record:
                total_months = int(row['total_months'])
                start_date = startDate

                # Loop to create 15 installments (5 years * 3 installments per year)
                for i in range(1, 16):
                    # Set start and end dates for each installment
                    if i == 1:
                        current_start_date = start_date
                    else:
                        current_start_date = previous_end_date + datetime.timedelta(days=30)

                    current_end_date = current_start_date + datetime.timedelta(days=90)

                    # Create installment dictionary
                    installment = {
                        'sr_no': i,
                        'period': total_months,
                        'start_period': current_start_date.strftime('%Y-%m-%d'),
                        'end_period': current_end_date.strftime('%Y-%m-%d'),
                        'due_date': (current_end_date + datetime.timedelta(days=60)).strftime('%Y-%m-%d'),
                        'balance': 42000,  # Adjust balance if necessary
                        'installment_number': i,
                        'paid': row.get(f'paid_or_not_installment_{i}', 'Not Available')  # Adjust field accordingly
                    }

                    installment_list.append(installment)
                    previous_end_date = current_end_date

                # Calculate total period and balance for all installments
                total_period += total_months  # Assuming total_months is consistent for each installment
                total_balance += 42000  # Assuming balance remains constant; adjust as necessary

        # Fetch other necessary details
        cursor.execute("SELECT fellowship_withdrawn FROM signup WHERE email=%s", (email,))
        output = cursor.fetchall()

        # print(installments)

        payment_statuses = {}
        latest_paid = 0

        # Loop through installment numbers (from 1 to 15)
        for i in range(1, 16):
            status_key = f'status_paid_{i}'  # e.g., status_paid_1, status_paid_2
            query = f"SELECT {status_key} FROM installments WHERE email=%s"
            cursor.execute(query, (email,))
            result_paid = cursor.fetchone()
            # Check if a result was returned and store the payment status
            if result_paid is not None:
                payment_status = result_paid[status_key]  # Get the payment status from the result tuple
            else:
                payment_status = None  # Handle case where no result is found

            payment_statuses[i] = payment_status  # Map installment number to its status

            if payment_statuses.get(i) == 'Paid':
                latest_paid = i

        # Pass this dictionary to your template context
        context = {
            'payment_statuses': payment_statuses,
            'latest_paid': latest_paid,  # Pass the latest paid installment
        }

        # Check if the user is approved for fellowship no matter the year to show the desired sidebar.
        if records['final_approval'] == 'accepted':
            finally_approved = 'approved'
        else:
            finally_approved = 'pending'

        if records:
            user = records['first_name'] + ' ' + records['last_name']
            photo = records['applicant_photo']
        else:
            user = "Admin"
            photo = '/static/assets/img/default_user.png'

        cnx.commit()
        cursor.close()
        cnx.close()

        return render_template('CandidatePages/installment_details.html', title="Installment Details",
                               records=records, record=record, output=output,
                               installment_list=installment_list, user=user,
                               total_period=total_period, total_balance=total_balance,
                               today=today, installments=installments, year=year, **context,
                               finally_approved=finally_approved, photo=photo
                               )

    @installments_blueprint.route('/submit_installments', methods=['GET', 'POST'])
    def submit_installments():
        """
        This function is used on the installment_userpage.html Page.
        The function is used for submitting the installments for the Old Users who have PHD Registration year
        before 2023.
        :return:
        """
        # Database connection
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        if request.method == 'POST':
            email = session.get('email')  # Use .get() to avoid KeyError if 'email' is not in session
            inst_num = request.form.get('inst_num')
            start_period = request.form.get('start_period')
            end_period = request.form.get('end_period')
            recieved_pay = request.form.get('recieved_pay')
            recieved_date = request.form.get('recieved_date')
            recieved_day = request.form.get('recieved_day')

            try:
                # Check if the email already exists in the installments table
                check_query = "SELECT * FROM installments WHERE email = %s"
                cursor.execute(check_query, (email,))
                result = cursor.fetchone()

                if result:
                    # Check if each installment slot is completely filled
                    installment_2_filled = (result['start_period_2'] and
                                            result['end_period_2'] and
                                            result['recieved_pay_2'] and
                                            result['recieved_date_2'])
                    installment_3_filled = (result['start_period_3'] and
                                            result['end_period_3'] and
                                            result['recieved_pay_3'] and
                                            result['recieved_date_3'])
                    installment_4_filled = (result['start_period_4'] and
                                            result['end_period_4'] and
                                            result['recieved_pay_4'] and
                                            result['recieved_date_4'])
                    installment_5_filled = (result['start_period_5'] and
                                            result['end_period_5'] and
                                            result['recieved_pay_5'] and
                                            result['recieved_date_5'])

                    if not installment_2_filled:
                        update_query = """
                            UPDATE installments
                            SET inst_num_2 = %s, start_period_2 = %s, end_period_2 = %s, 
                                recieved_pay_2 = %s, recieved_date_2 = %s, received_day_2 = %s,  status_paid_2 = %s
                            WHERE email = %s
                        """
                        values = (2, start_period, end_period, recieved_pay, recieved_date, recieved_day, 'Paid', email)
                    elif not installment_3_filled:
                        update_query = """
                            UPDATE installments
                            SET inst_num_3 = %s, start_period_3 = %s, end_period_3 = %s, 
                                recieved_pay_3 = %s, recieved_date_3 = %s, received_day_3 = %s,status_paid_3 = %s
                            WHERE email = %s
                        """
                        values = (3, start_period, end_period, recieved_pay, recieved_date, recieved_day, 'Paid', email)
                    elif not installment_4_filled:
                        update_query = """
                            UPDATE installments
                            SET inst_num_4 = %s, start_period_4 = %s, end_period_4 = %s, 
                                recieved_pay_4 = %s, recieved_date_4 = %s, received_day_4 = %s, status_paid_4 = %s
                            WHERE email = %s
                        """
                        values = (4, start_period, end_period, recieved_pay, recieved_date, recieved_day, 'Paid', email)
                    elif not installment_5_filled:
                        update_query = """
                            UPDATE installments
                            SET inst_num_5 = %s, start_period_5 = %s, end_period_5 = %s, 
                                recieved_pay_5 = %s, recieved_date_5 = %s, received_day_5 = %s, status_paid_5 = %s
                            WHERE email = %s
                        """
                        values = (5, start_period, end_period, recieved_pay, recieved_date, recieved_day, 'Paid', email)
                    else:
                        return "Maximum installments reached", 400

                    cursor.execute(update_query, values)
                    message = "Installment updated successfully"
                    flash(message, 'success')
                else:
                    print('I am here')
                    # If email does not exist, insert a new record
                    insert_query = """
                        INSERT INTO installments (email, inst_num_1, start_period_1, end_period_1, 
                                                  recieved_pay_1, recieved_date_1, received_day_1, status_paid_1)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    values = (
                    email, inst_num, start_period, end_period, recieved_pay, recieved_date, recieved_day, 'Paid')
                    print(values)
                    cursor.execute(insert_query, values)
                    message = "Installment submitted successfully"
                    flash(message, 'success')

                cnx.commit()
                return redirect(url_for('installment_userpage'))
            except Exception as e:
                cnx.rollback()
                return f"An error occurred: {str(e)}", 500
            finally:
                cursor.close()
                cnx.close()

        return redirect(url_for('installment_userpage'))
