from datetime import date, timedelta, datetime
import mysql.connector
from classes.database import HostConfig, ConfigPaths, ConnectParam
import os
from flask_mail import Mail, Message
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from authentication.middleware import auth

issue_raised_blueprint = Blueprint('issue_raised', __name__)


def issue_raised_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @issue_raised_blueprint.route('/admin_issue_raised_by_students', methods=['GET'])
    def admin_issue_raised_by_students():
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('adminlogin.admin_login'))

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """SELECT * FROM issue_raised """
        cursor.execute(sql)
        # Fetch all records matching the query
        records = cursor.fetchall()
        # print(records)
        # Close the cursor and database connection
        cursor.close()
        cnx.close()
        return render_template('AdminPages/issue_raised.html', records=records)