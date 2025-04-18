from collections import defaultdict
from datetime import date, timedelta, datetime
import mysql.connector
from classes.database import HostConfig, ConfigPaths, ConnectParam
import os
from flask_mail import Mail, Message
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from authentication.middleware import auth

withdraw_application_blueprint = Blueprint('withdraw_application', __name__)


def withdraw_application_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @withdraw_application_blueprint.route('/withdrawed_application_admin', methods=['GET', 'POST'])
    def withdrawed_application_admin():
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('adminlogin.admin_login'))

        email = session.get('email')

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        # Fetch the relevant information
        select_query = """
            SELECT s.*, ap.*
            FROM signup s
            LEFT JOIN application_page ap ON s.email = ap.email
            WHERE s.request_withdrawal = '1'
        """
        cursor.execute(select_query)
        result_set = cursor.fetchall()

        result_set_by_year = defaultdict(list)
        phd_date = None
        var = None
        for result in result_set:
            if result['request_withdrawal'] == 1:
                var = 'Raised for Withdrawal'
                registration_year = result['phd_registration_year']
                result_set_by_year[registration_year].append(result)
        sorted_years = sorted(result_set_by_year.keys(), reverse=True)

        application_2023 = """
                    SELECT s.*, ap.*
                    FROM signup s
                    LEFT JOIN application_page ap ON s.email = ap.email
                    WHERE s.request_withdrawal = '1' and ap.fellowship_application_year = '2023'
                """
        cursor.execute(application_2023)
        result2023 = cursor.fetchall()

        application_2022 = """
                SELECT s.*, ap.*
                FROM signup s
                LEFT JOIN application_page ap ON s.email = ap.email
                WHERE s.request_withdrawal = '1' and ap.fellowship_application_year = '2022'
            """
        cursor.execute(application_2022)
        result2022 = cursor.fetchall()

        application_2021 = """
                    SELECT s.*, ap.*
                    FROM signup s
                    LEFT JOIN application_page ap ON s.email = ap.email
                    WHERE s.request_withdrawal = '1' and ap.fellowship_application_year = '2021'
                """
        cursor.execute(application_2021)
        result2021 = cursor.fetchall()

        application_2020 = """
                    SELECT s.*, ap.*
                    FROM signup s
                    LEFT JOIN application_page ap ON s.email = ap.email
                    WHERE s.request_withdrawal = '1' and ap.fellowship_application_year = '2020'
                """
        cursor.execute(application_2020)
        result2020 = cursor.fetchall()

        cursor.close()
        cnx.close()
        return render_template('AdminPages/withdrawed_application_admin.html', result_set=result_set, var=var,
                               sorted_years=sorted_years, result_set_by_year=result_set_by_year,
                               result2023=result2023, result2022=result2022, result2021=result2021,
                               result2020=result2020)