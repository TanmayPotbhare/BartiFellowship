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

    @document_repo_blueprint.route('/document_repo', methods=['GET', 'POST'])
    def document_repo():
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        # Queries to get district data for the map
        query = """SELECT * FROM application_page"""
        # Execute district count query
        cursor.execute(query,)
        results = cursor.fetchall()
        cnx.commit()
        cursor.close()
        cnx.close()
        return render_template('AdminPages/document_repo.html', results=results)