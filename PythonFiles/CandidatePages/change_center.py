from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response
from Authentication.middleware import auth
import datetime

change_center_blueprint = Blueprint('change_center', __name__)


def change_center_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @change_center_blueprint.route('/change_center', methods=['GET', 'POST'])
    def change_center():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        if session.get('change_center'):
            # Redirect to the admin login page if the user is not logged in
            flash('Center Name has been changed successfully', 'success')

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """SELECT * FROM application_page WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchone()

        # Check if the user is approved for fellowship no matter the year to show the desired sidebar.
        if records['final_approval'] == 'accepted':
            finally_approved = 'approved'
        else:
            finally_approved = 'pending'

        # Pass the user and Photo to the header and the template to render is neatly instead of keeping it in session.
        if records:
            user = records['first_name'] + ' ' + records['last_name']
            photo = records['applicant_photo']
        else:
            user = "Admin"
            photo = '/static/assets/img/default_user.png'
        return render_template('CandidatePages/change_center.html', title="Change Center Details", records=records,
                               user=user, photo=photo, finally_approved=finally_approved)

    @change_center_blueprint.route('/change_center_submit', methods=['GET', 'POST'])
    def change_center_submit():
        email = session['email']
        # print('Joining Email', email)
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """SELECT name_of_college, first_name, last_name FROM application_page WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchone()

        if request.method == 'POST':
            name_of_college_old_value = records['name_of_college']
            name_of_college = request.form['name_of_college']
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Fixed format for date
            current_time = datetime.datetime.now().strftime('%H:%M:%S')  # Fixed format for time

            # Handle case where joining_report is not already uploaded

            update_query = """UPDATE application_page 
                                          SET name_of_college=%s, name_of_college_old_value=%s,
                                          name_of_college_changed_date=%s, name_of_college_changed_time=%s 
                                          WHERE email = %s
                                  """
            cursor.execute(update_query,
                           (name_of_college, name_of_college_old_value, current_date, current_time, email))
            cnx.commit()

            cursor.close()
            cnx.close()

            session['change_center'] = True
            return redirect(url_for('change_center.change_center'))

        else:
            cursor.close()
            cnx.close()
            return redirect(url_for('change_center.change_center'))  # Redirect for non-POST requests