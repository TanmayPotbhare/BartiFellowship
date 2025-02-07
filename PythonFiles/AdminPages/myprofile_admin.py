from flask import Blueprint, render_template, session, request, redirect, url_for, flash, jsonify, make_response
from PythonFiles.AdminPages.Dashboard.dashboardCount_functions import *
from PythonFiles.AdminPages.Dashboard.export_column_names import COMMON_COLUMNS, COMMON_HEADERS

myprofile_admin_blueprint = Blueprint('myprofile_admin', __name__)


def myprofile_admin_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @myprofile_admin_blueprint.route('/myprofile_admin')
    def myprofile_admin():
        user = session['user']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute("SELECT * FROM admin WHERE username = %s", (user,))
        result = cursor.fetchone()
        # print(result)
        cnx.commit()
        cursor.close()
        cnx.close()
        return render_template('AdminPages/myprofile_admin.html', result=result)