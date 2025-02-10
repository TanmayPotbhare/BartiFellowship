from datetime import date, timedelta, datetime
import mysql.connector
from Classes.database import HostConfig, ConfigPaths, ConnectParam
import os
from flask_mail import Mail, Message
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from Authentication.middleware import auth


fellowshipdetails_blueprint = Blueprint('fellowshipdetails', __name__)


def fellowshipdetails_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @fellowshipdetails_blueprint.route('/fellowship_details/<string:email>', methods=['GET', 'POST'])
    def fellowship_details(email):
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        today = datetime.today().date()

        cursor.execute("SELECT * FROM application_page where email=%s ", (email,))
        result = cursor.fetchall()
        startDate = result[0]['final_approved_date']

        cursor.execute("SELECT * FROM installments where email=%s", (email,))
        installments = cursor.fetchall()
        print('installments', installments)

        cursor.execute("SELECT * FROM payment_sheet WHERE email=%s", (email,))
        record = cursor.fetchall()

        # Assuming only one row in record
        for row in record:
            total_months = int(row['total_months'])
            start_date = startDate
            installment_list = []

            # Loop to create 15 installments (5 years * 3 installments per year)
            for i in range(1, 16):
                # Set start and end dates for each installment
                if i == 1:
                    current_start_date = start_date
                else:
                    current_start_date = previous_end_date + timedelta(days=30)

                current_end_date = current_start_date + timedelta(days=90)

                # Create installment dictionary
                installment = {
                    'sr_no': i,
                    'period': total_months,
                    'start_period': current_start_date.strftime('%Y-%m-%d'),
                    'end_period': current_end_date.strftime('%Y-%m-%d'),
                    'due_date': (current_end_date + timedelta(days=60)).strftime('%Y-%m-%d'),
                    'balance': 42000,  # Adjust balance if necessary
                    'installment_number': i,
                    'paid': row.get(f'paid_or_not_installment_{i}', 'Not Available')
                    # Assuming the field changes per installment
                }

                # Append to installment list
                installment_list.append(installment)
                # print(installments)
                # Update previous_end_date for the next iteration
                previous_end_date = current_end_date

            # Calculate total period and total balance for all installments
            total_period = sum(inst['period'] for inst in installment_list)
            total_balance = sum(inst['balance'] for inst in installment_list)

            for installment in installment_list:
                # Convert and format the dates
                start_period = datetime.strptime(installment['start_period'], '%Y-%m-%d').strftime('%d %B %Y')
                end_period = datetime.strptime(installment['end_period'], '%Y-%m-%d').strftime('%d %B %Y')
                installment['formatted_start_period'] = start_period
                installment['formatted_end_period'] = end_period

        cursor.execute("SELECT fellowship_withdrawn FROM signup where email=%s", (email,))
        output = cursor.fetchall()

        installment_button_status = []
        previously_paid = False  # Track if the previous installment was paid

        # Loop through 15 installments directly
        for current_installment_number in range(1, 16):
            status_paid = None

            # Check the status of the current installment
            for installment in installments:
                if installment.get(f'inst_num_{current_installment_number}') == current_installment_number:
                    status_paid = installment.get(f'status_paid_{current_installment_number}')

            # Ensure the first installment can be paid if not already paid
            if current_installment_number == 1:
                if status_paid == 'Paid':
                    installment_button_status.append('paid')
                    previously_paid = True
                else:
                    installment_button_status.append('pay_enabled')  # First installment always enabled
                    previously_paid = False
            else:
                # Handle installments after the first
                if status_paid == 'Paid':
                    installment_button_status.append('paid')
                    previously_paid = True
                elif previously_paid:
                    installment_button_status.append('pay_enabled')  # Enable pay if previous is paid
                else:
                    installment_button_status.append('disabled')  # Disable if previous is unpaid

        # Example to print out installment statuses
        for i, button_status in enumerate(installment_button_status):
            print(f"Installment {i + 1}: {button_status}")

        cnx.commit()
        cursor.close()
        cnx.close()

        return render_template(
            'AdminPages/PaymentSheet/fellowship_details.html',
            result=result,
            record=record,
            output=output,
            installment_list=installment_list,
            total_period=total_period,
            total_balance=total_balance,
            today=today,
            installments=installments,
            installment_button_status=installment_button_status
        )

    @fellowshipdetails_blueprint.route('/pay_installment/<int:inst_no>', methods=['POST'])
    def pay_installment(inst_no):
        """
        This function is used on the fellowship_details.html Page.
        The function pays installments to the students by Installment Number.
        """
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        if request.method == 'POST':
            email = session.get('email')
            start_period = request.form.get('start_period')
            end_period = request.form.get('end_period')
            received_pay = request.form.get('received_pay')
            installment_number = request.form.get('installment_number')
            # Get the current date and format it
            current_date = datetime.now().date()  # Current date
            received_day = current_date.strftime('%A')  # Current day name (e.g., 'Monday')

            print(
                f"Email: {email}, Start: {start_period}, End: {end_period}, Received Pay: {received_pay}, Received Date: {current_date}")

            # Check if the email already exists
            cursor.execute("SELECT * FROM installments WHERE email = %s", (email,))
            user_record = cursor.fetchone()

            if user_record:  # Email exists
                # Check if the installment already exists
                for i in range(1, 5):  # Check inst_num to inst_num_4
                    if user_record[f'inst_num_{i}'] == inst_no:
                        # Installment already exists, exit or handle accordingly
                        return "Installment details already exist.", 400

                # If not found, find the first available installment column to insert
                for i in range(1, 16):
                    if user_record[f'inst_num_{i}'] is None:  # Check for None
                        cursor.execute(f"""
                                UPDATE installments
                                SET inst_num_{i} = %s, start_period_{i} = %s, end_period_{i} = %s,
                                recieved_pay_{i} = %s, recieved_date_{i} = %s, received_day_{i} = %s, status_paid_{i} = 'Paid'
                                WHERE email = %s
                            """, (inst_no, start_period, end_period, received_pay, current_date, received_day, email))
                        print(
                            f"Updated: inst_num_{i} with {inst_no}, start_period_{i} with {start_period}")  # Debugging output
                        break
            else:  # Email does not exist, insert a new record

                cursor.execute("""
                        INSERT INTO installments (email, inst_num_1, start_period_1, end_period_1, 
                        recieved_pay_1, recieved_date_1, received_day_1, status_paid_1) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, 'Paid')
                    """, (email, inst_no, start_period, end_period, received_pay, current_date, received_day))

                print(f"Inserted new record for {email} with inst_num: {inst_no}")  # Debugging output

            cnx.commit()  # Commit the changes
            cursor.close()  # Close the cursor
            cnx.close()  # Close the connection

            return "Installment paid successfully.", 200

    @fellowshipdetails_blueprint.route('/submit_installments_admin', methods=['GET', 'POST'])
    def submit_installments_admin():
        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        if request.method == 'POST':
            email = session.get('email')  # Use .get() to avoid KeyError if 'email' is not in session
            start_period = request.form.get('start_period')
            end_period = request.form.get('end_period')
            recieved_pay = request.form.get('recieved_pay')
            recieved_date = request.form.get('recieved_date')

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
                                            result['recieved_payy_3'] and
                                            result['recieved_date_3'])
                    installment_4_filled = (result['start_period_4'] and
                                            result['end_period_4'] and
                                            result['recieved_pay_4'] and
                                            result['recieved_date_4'])

                    if not installment_2_filled:
                        update_query = """
                                UPDATE installments
                                SET inst_num_2 = %s, start_period_2 = %s, end_period_2 = %s, 
                                    recieved_pay_2 = %s, recieved_date_2 = %s, status_paid_2 = %s
                                WHERE email = %s
                            """
                        values = (2, start_period, end_period, recieved_pay, recieved_date, 'Paid', email)
                    elif not installment_3_filled:
                        update_query = """
                                UPDATE installments
                                SET inst_num_3 = %s, start_period_3 = %s, end_period_3 = %s, 
                                    recieved_pay_3 = %s, recieved_date_3 = %s, status_paid_3 = %s
                                WHERE email = %s
                            """
                        values = (3, start_period, end_period, recieved_pay, recieved_date, 'Paid', email)
                    elif not installment_4_filled:
                        update_query = """
                                UPDATE installments
                                SET inst_num_4 = %s, start_period_4 = %s, end_period_4 = %s, 
                                    recieved_pay_4 = %s, recieved_date_4 = %s, status_paid_4 = %s
                                WHERE email = %s
                            """
                        values = (4, start_period, end_period, recieved_pay, recieved_date, 'Paid', email)
                    else:
                        return "Maximum installments reached", 400

                    cursor.execute(update_query, values)
                    message = "Installment updated successfully"
                    flash(message, 'success')
                else:
                    # If email does not exist, insert a new record
                    insert_query = """
                            INSERT INTO installments (email, inst_num, start_period, end_period, 
                                                      recieved_pay, recieved_date, status_paid)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
                    values = (email, 1, start_period, end_period, recieved_pay, recieved_date, 'Paid')
                    cursor.execute(insert_query, values)
                    message = "Installment submitted successfully"
                    flash(message, 'success')

                cnx.commit()
                return redirect(url_for('fellowshipdetails.fellowship_details', email=email))
            except Exception as e:
                cnx.rollback()
                return f"An error occurred: {str(e)}", 500
            finally:
                cursor.close()
                cnx.close()

        return redirect(url_for('fellowshipdetails.fellowship_details', email=email))