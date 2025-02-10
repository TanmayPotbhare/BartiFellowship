from datetime import date, timedelta
import mysql.connector
from Classes.database import HostConfig, ConfigPaths, ConnectParam
import os
from flask_mail import Mail, Message
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from Authentication.middleware import auth

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
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('adminlogin.admin_login'))

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        record = None  # Initialize record with a default value or None
        email_list = None
        if request.method == 'POST':
            year = request.form['year']
            print(year)
            sql = """ SELECT email FROM signup WHERE year=%s"""
            cursor.execute(sql, (year,))
            record = cursor.fetchall()
            print(record)
            # Process the records as needed
            email_list = [entry['email'] for entry in record]
            print(email_list)
        cursor.close()
        cnx.close()

        return render_template('AdminPages/sendbulkemails.html', record=record, email_list=email_list)
