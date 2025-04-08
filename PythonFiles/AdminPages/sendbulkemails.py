from datetime import date, timedelta
import mysql.connector
from classes.database import HostConfig, ConfigPaths, ConnectParam
import os
from flask_mail import Mail, Message
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from authentication.middleware import auth
from flask import jsonify

bulkemails_blueprint = Blueprint('bulkemails', __name__)


def bulkemails_auth(app, mail):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @bulkemails_blueprint.route('/sendbulkEmails', methods=['GET', 'POST'])
    def sendbulkEmails():
        if not session.get('logged_in'):
            return redirect(url_for('adminlogin.admin_login'))

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        record = None
        email_list = None
        num_emails = 0

        if request.method == 'POST':
            year = request.form['year']
            form_status = request.form['form_status']
            candidate_status = request.form.get('candidate_status') # Use .get() to handle missing values
            print("Bulk email Year : ", year)
            print("Bulk email Form Status : ", form_status)
            print("Bulk email Candidate Status : ", candidate_status)

            sql = """
                SELECT
                    s.email
                FROM
                    signup s
                JOIN
                    BartiApplication.application_page ap ON s.email = ap.email
                WHERE
                    s.year = %s
                """
            sql_params = [year]
            where_conditions = []

            if form_status == "":  # User selected "Incomplete" (maps to NULL in DB)
                where_conditions.append("ap.application_form_status IS NULL")
            elif form_status == "submitted":  # User selected "Completed"
                where_conditions.append("ap.application_form_status = %s")
                sql_params.append(form_status)

            if candidate_status:  # Check if candidate_status has a value
                where_conditions.append("ap.final_approval = %s")
                sql_params.append(candidate_status)

            if where_conditions:
                sql += " AND " + " AND ".join(where_conditions)
            try:
                cursor.execute(sql, tuple(sql_params))
                record = cursor.fetchall()
                email_list = [entry['email'] for entry in record]
                num_emails = len(email_list)
                print(f"Number of emails found: {num_emails}")
                print("Email List (POST):", email_list)
                if num_emails == 0:
                    flash("No records found", 'info')
            except Exception as e:
                        print(f"Database error: {e}")
                        flash("Error fetching records", 'danger')
                        email_list = []
                        num_emails = 0
            finally:
                cursor.close()
                cnx.close()
                return jsonify(email_list=email_list)  # Return JSON for AJAX

        elif request.method == 'GET':
            try:
                cursor.close()
                cnx.close()
            except Exception as e:
                print(f"Error closing database connection (GET): {e}")
            return render_template('AdminPages/sendbulkemails.html', record=record, email_list=email_list, num_emails=num_emails)

        try:
            cursor.close()
            cnx.close()
        except Exception as e:
            print(f"Error closing database connection (fallback): {e}")
        return "Error: Invalid request method"
