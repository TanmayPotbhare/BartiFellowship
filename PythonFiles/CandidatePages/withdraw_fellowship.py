from Classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response
from Authentication.middleware import auth

withdraw_fellowship_blueprint = Blueprint('withdraw_fellowship', __name__)


def withdraw_fellowship_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @withdraw_fellowship_blueprint.route('/withdraw_fellowship', methods=['GET', 'POST'])
    def withdraw_fellowship():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """SELECT * FROM application_page WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchall()

        # Check if the user is approved for fellowship no matter the year to show the desired sidebar.
        if records[0]['final_approval'] == 'accepted':
            finally_approved = 'approved'
        else:
            finally_approved = 'pending'

        # Pass the user and Photo to the header and the template to render is neatly instead of keeping it in session.
        if records:
            user = records[0]['first_name'] + ' ' + records[0]['last_name']
            photo = records[0]['applicant_photo']
        else:
            user = "Admin"
            photo = '/static/assets/img/default_user.png'
        return render_template('CandidatePages/withdraw_fellowship.html', title="Withdraw Fellowship", records=records,
                               user=user, photo=photo, finally_approved=finally_approved)