from datetime import date, timedelta, datetime
from io import BytesIO
import mysql
from openpyxl.workbook import Workbook
from openpyxl.styles import Font
from classes.database import HostConfig, ConfigPaths, ConnectParam
from fpdf import FPDF
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response, jsonify


payment_approval_blueprint = Blueprint('payment_approval', __name__)

def payment_approval_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    def admin_accept_payment_sheet_status(cnx, cursor, year, sheet_id, status, user): # Added cnx and cursor
        if year:
            database = f'payment_sheet_{year}'

            try:
                if user == 'Head of Department':
                    admin_action = 'Approved by Head of Department'
                    update_query = f"UPDATE `{database}` SET hod_approval = %s, hod_action = %s WHERE number = %s"
                elif user == 'Account Officer':
                    admin_action = 'Approved by Account Officer'
                    update_query = f"UPDATE `{database}` SET ao_approval = %s, ao_action = %s WHERE number = %s"
                elif user == 'Registrar':
                    admin_action = 'Approved by Registrar'
                    update_query = f"UPDATE `{database}` SET registrar_approval = %s, registrar_action = %s WHERE number = %s"
                else:
                    admin_action = 'Approved by Admin'
                    update_query = f"UPDATE `{database}` SET admin_approval = %s, admin_action = %s WHERE number = %s"

                cursor.execute(update_query, (status, admin_action, sheet_id))
                cnx.commit()
                print("Status Updated")
            except mysql.connector.Error as err:
                print(f"Error updating status: {err}")
                cnx.rollback() # Rollback on error
                flash('An error occurred while updating status.', 'error') # Flash message


    def admin_reject_payment_sheet_status(cnx, cursor, year, sheet_id, status, rejection_reason, user): # Added cnx and cursor
        if year:
            database = f'payment_sheet_{year}'

            try:
                if user == 'Head of Department':
                    admin_action = 'Rejected by Head of Department'
                    update_query = f"UPDATE `{database}` SET hod_approval = %s, hod_reject_reason = %s, hod_action = %s WHERE number = %s"
                elif user == 'Account Officer':
                    admin_action = 'Rejected by Account Officer'
                    update_query = f"UPDATE `{database}` SET ao_approval = %s, ao_reject_reason = %s, ao_action = %s WHERE number = %s"
                elif user == 'Registrar':
                    admin_action = 'Rejected by Registrar'
                    update_query = f"UPDATE `{database}` SET registrar_approval = %s, registrar_reject_reason = %s, registrar_action = %s WHERE number = %s"
                else:
                    admin_action = 'Rejected by Admin'
                    update_query = f"UPDATE `{database}` SET admin_approval = %s, admin_reject_reason = %s, admin_action = %s WHERE number = %s"

                cursor.execute(update_query, (status, rejection_reason, admin_action, sheet_id))
                cnx.commit() # Commit the transaction
                print("Status Updated")
            except mysql.connector.Error as err:
                print(f"Error updating status: {err}")
                cnx.rollback() # Rollback on error
                flash('An error occurred while updating status.', 'error') # Flash message

    def admin_hold_payment_sheet_status(cnx, cursor, year, sheet_id, status, hold_reason, user): # Added cnx and cursor
        if year:
            database = f'payment_sheet_{year}'

            try:

                if user == 'Head of Department':
                    admin_action = 'On Hold by Head of Department'
                    update_query = f"UPDATE `{database}` SET hod_approval = %s, hod_hold_reason = %s, hod_action = %s WHERE number = %s"
                elif user == 'Account Officer':
                    admin_action = 'On Hold by Account Officer'
                    update_query = f"UPDATE `{database}` SET ao_approval = %s, ao_hold_reason = %s, ao_action = %s WHERE number = %s"
                elif user == 'Registrar':
                    admin_action = 'On Hold by Registrar'
                    update_query = f"UPDATE `{database}` SET registrar_approval = %s, registrar_hold_reason = %s, registrar_action = %s WHERE number = %s"
                else:
                    admin_action = 'On Hold by Admin'
                    update_query = f"UPDATE `{database}` SET admin_approval = %s, admin_hold_reason = %s, admin_action = %s WHERE number = %s"

                cursor.execute(update_query, (status, hold_reason, admin_action, sheet_id))
                cnx.commit() # Commit the transaction
                print("Status Updated")
            except mysql.connector.Error as err:
                print(f"Error updating status: {err}")
                cnx.rollback() # Rollback on error
                flash('An error occurred while updating status.', 'error') # Flash message

    @payment_approval_blueprint.route('/admin_accept_payment_sheet', methods=['POST'])  # Corrected method
    def admin_accept_payment_sheet():
        if not session.get('logged_in'):
            flash('Please log in.', 'error')
            return redirect(url_for('adminlogin.admin_login'))

        user = session['user']
        fellowship_awarded_year = request.form.get('fellowship_awarded_year')
        print("The user is " + user)

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        try:
            sheet_id = request.form['sheet_id']
            status = 'accepted'
            print('I am ACCEPTING Sheet No:', sheet_id)

            fetch_admin = "SELECT year FROM admin WHERE username = %s"
            cursor.execute(fetch_admin, (user,))
            admin_details = cursor.fetchone()

            if admin_details:
                year_string = admin_details['year']
                try:
                    if user in ['Head of Department', 'Account Officer', 'Registrar']:
                        year = fellowship_awarded_year
                    else:
                        year = int(year_string.split(' ')[1])
                    print("Accepting for Year:", year)
                    admin_accept_payment_sheet_status(cnx, cursor, year, sheet_id, status, user)  # Pass cnx and cursor
                    flash('Payment sheet accepted successfully!', 'success')
                except (IndexError, ValueError):
                    print("Invalid year format in admin details.")
                    flash('Invalid year format in admin details.', 'error')
            else:
                print("Admin not found")
                flash('Admin not found.', 'error')

        except Exception as e:
            print(f"Error in admin_accept_payment_sheet: {e}")
            flash('An error occurred during acceptance.', 'error')  # Flash message

        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()

        return redirect(url_for('payment_sheet.payment_sheet'))

    @payment_approval_blueprint.route('/admin_reject_payment_sheet', methods=['GET', 'POST'])
    def admin_reject_payment_sheet():
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('adminlogin.admin_login'))

        user = session['user']
        fellowship_awarded_year = request.form.get('fellowship_awarded_year')
        print("The user is " + user)

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        try:
            sheet_id = request.form['sheet_id']
            rejection_reason = request.form['rejectionReason']
            status = 'rejected'
            print('I am REJECTING Sheet No:', sheet_id)
            print('Rejection reason is:', rejection_reason)

            fetch_admin = "SELECT year FROM admin WHERE username = %s"
            cursor.execute(fetch_admin, (user,))
            admin_details = cursor.fetchone()

            if admin_details:
                year_string = admin_details['year']
                try:
                    if user in ['Head of Department', 'Account Officer', 'Registrar']:
                        year = fellowship_awarded_year
                    else:
                        year = int(year_string.split(' ')[1])
                    print("Accepting for Year:", year)
                    admin_reject_payment_sheet_status(cnx, cursor, year, sheet_id, status,
                                                      rejection_reason, user)  # Pass cnx and cursor
                    flash('Payment sheet rejected successfully!', 'success')
                except (IndexError, ValueError):
                    print("Invalid year format in admin details.")
                    flash('Invalid year format in admin details.', 'error')
            else:
                print("Admin not found")
                flash('Admin not found.', 'error')

        except Exception as e:
            print(f"Error in admin_reject_payment_sheet: {e}")
            flash('An error occurred during rejecting candidate.', 'error')  # Flash message

        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()

        return redirect(url_for('payment_sheet.payment_sheet'))

    @payment_approval_blueprint.route('/admin_hold_payment_sheet', methods=['GET', 'POST'])
    def admin_hold_payment_sheet():
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('adminlogin.admin_login'))

        user = session['user']
        fellowship_awarded_year = request.form.get('fellowship_awarded_year')
        print("The user is " + user)

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        try:
            sheet_id = request.form['sheet_id']
            on_hold_reason = request.form['onHoldReason']
            status = 'hold'
            print('I am HOLDING Sheet No:', sheet_id)
            print('On Hold reason is:', on_hold_reason)

            fetch_admin = "SELECT year FROM admin WHERE username = %s"
            cursor.execute(fetch_admin, (user,))
            admin_details = cursor.fetchone()

            if admin_details:
                year_string = admin_details['year']
                try:
                    if user in ['Head of Department', 'Account Officer', 'Registrar']:
                        year = fellowship_awarded_year
                    else:
                        year = int(year_string.split(' ')[1])
                    print("Accepting for Year:", year)
                    admin_hold_payment_sheet_status(cnx, cursor, year, sheet_id, status,
                                                    on_hold_reason, user)  # Pass cnx and cursor
                    flash('Payment sheet kept On Hold successfully!', 'success')
                except (IndexError, ValueError):
                    print("Invalid year format in admin details.")
                    flash('Invalid year format in admin details.', 'error')
            else:
                print("Admin not found")
                flash('Admin not found.', 'error')

        except Exception as e:
            print(f"Error in admin_hold_payment_sheet: {e}")
            flash('An error occurred during acceptance.', 'error')  # Flash message

        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()

        return redirect(url_for('payment_sheet.payment_sheet'))