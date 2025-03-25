from datetime import timedelta, date
from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, jsonify

document_repo_blueprint = Blueprint('document_repo', __name__)


def document_repo_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    # @document_repo_blueprint.route('/document_repo', methods=['GET', 'POST'])
    # def document_repo():
    #     host = HostConfig.host
    #     connect_param = ConnectParam(host)
    #     cnx, cursor = connect_param.connect(use_dict=True)

    #     # Queries to get district data for the map
    #     query = """SELECT * FROM application_page"""
    #     # Execute district count query
    #     cursor.execute(query,)
    #     results = cursor.fetchall()
    #     cnx.commit()
    #     cursor.close()
    #     cnx.close()
    #     return render_template('AdminPages/document_repo.html', results=results)
    
    @document_repo_blueprint.route('/document_repo', methods=['GET', 'POST'])
    def document_repo():
        if not session.get('logged_in'):
            return redirect(url_for('adminlogin.admin_login'))

        user = session['user']
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute("SELECT * FROM admin WHERE username = %s", (user,))
        admin_result = cursor.fetchone()
        admin_year = admin_result['year']
        admin_username = admin_result['username']
        role = admin_result['role']

        year_selected = None

        if role == "Admin" and admin_username == "Admin2021" and admin_year == "BANRF 2021":
            year_selected = "2021"
        elif role == "Admin" and admin_username == "Admin2022" and admin_year == "BANRF 2022":
            year_selected = "2022"
        elif role == "Admin" and admin_username == "Admin2023" and admin_year == "BANRF 2023":
            year_selected = "2023"
        elif role == "Admin" and admin_username == "Admin2024" and admin_year == "BANRF.2024":
            year_selected = "2024"

        sql = """SELECT * FROM application_page"""

        if year_selected:
            sql += " WHERE phd_registration_year = %s"
            cursor.execute(sql, (year_selected,))
        else:
            # sql += " WHERE phd_registration_year IN ('2020', '2021', '2022', '2023', '2024')"
            cursor.execute(sql)

        results = cursor.fetchall()
        cnx.commit()
        cursor.close()
        cnx.close()
        return render_template('AdminPages/document_repo.html', results=results)