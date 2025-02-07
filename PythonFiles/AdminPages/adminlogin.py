import mysql.connector
from classes.database import HostConfig, ConfigPaths, ConnectParam
import os
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from authentication.middleware import auth

adminlogin_blueprint = Blueprint('adminlogin', __name__)


def adminlogin_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @adminlogin_blueprint.route('/adminlogin', methods=['GET', 'POST'])
    def admin_login():  # ------------------ ADMIN LOGIN
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']

            # Validate that both username and password are provided
            if not username or not password:
                flash('Please enter username and password.', 'error')
                cursor.close()
                cnx.close()
                return redirect(url_for('adminlogin.admin_login'))

            # Check if the user is an admin
            sql = "SELECT * FROM admin WHERE username=%s AND password=%s AND role=%s"
            cursor.execute(sql, (username, password, role))
            user = cursor.fetchone()
            print(user)
            cnx.commit()

            if not user:
                flash('Please enter valid username and password.', 'error')
                cursor.close()
                cnx.close()
                return redirect(url_for('adminlogin.admin_login'))

            session['user'] = user['username']

            if user:
                # Set session variable to indicate user is logged in
                session['logged_in'] = True
                # Close the connection and cursor
                cursor.close()
                cnx.close()
                return redirect(url_for('admin_dashboard.admin_dashboard'))
            else:
                error = 'Invalid username or password'
                # Close the connection and cursor
                cursor.close()
                cnx.close()
                flash('Please enter Valid Details to Login', 'error')
                return render_template('AdminPages/adminlogin.html', error=error)
        return render_template('AdminPages/adminlogin.html')

    @adminlogin_blueprint.route('/admin_logout', methods=['GET'])
    def admin_logout():  # ------------------ ADMIN LOGOUT
        # Clear the session
        session.clear()

        # Provide feedback and redirect to the login page
        flash('You have been logged out successfully.', 'success')
        return redirect(url_for('adminlogin.admin_login'))
