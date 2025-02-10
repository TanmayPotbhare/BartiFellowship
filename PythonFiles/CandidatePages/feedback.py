from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response
from Authentication.middleware import auth
import os
import datetime

feedback_blueprint = Blueprint('feedback', __name__)


def feedback_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @feedback_blueprint.route('/feedback', methods=['GET', 'POST'])
    def feedback():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        # if session.get('assessment'):
        #     # Redirect to the admin login page if the user is not logged in
        #     flash('Assessment Report has been uploaded successfully', 'success')

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
        return render_template('CandidatePages/feedback.html', title="Feedback", records=records,
                               user=user, photo=photo, finally_approved=finally_approved)

    @feedback_blueprint.route('/research_paper_submit', methods=['GET', 'POST'])
    def research_paper_submit():
        email = session['email']
        # print('Joining Email', email)
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """SELECT research_paper_feedback_file, first_name, last_name FROM application_page WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchone()

        first_name = records['first_name']
        last_name = records['last_name']

        if request.method == 'POST':
            research_paper_file = save_file_research_paper_feedback(request.files['research_paper_file'], first_name,
                                                              last_name)
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Fixed format for date
            current_time = datetime.datetime.now().strftime('%H:%M:%S')  # Fixed format for time

            # Handle case where joining_report is not already uploaded
            if not records.get('hra_utility_report'):
                update_query = """UPDATE application_page 
                                              SET research_paper_feedback_file=%s,
                                              research_paper_uploaded_date=%s, research_paper_uploaded_time=%s 
                                              WHERE email = %s
                                      """
                cursor.execute(update_query, (research_paper_file, current_date, current_time, email))
                cnx.commit()

                cursor.close()
                cnx.close()

                session['research_paper_feedback_file'] = True
                return redirect(url_for('feedback.feedback'))
            else:
                # Case where joining_report is already uploaded
                cursor.close()
                cnx.close()
                flash('Undertaking Report is Already Uploaded', 'Error')
                return "Undertaking report is already uploaded", 400
        else:
            cursor.close()
            cnx.close()
            return redirect(url_for('feedback.feedback'))  # Redirect for non-POST requests

    def save_file_research_paper_feedback(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['RESEARCH_PAPER_FEEDBACK'], filename))
            # return os.path.join(app.config['RENT_AGREEMENT_REPORT'], filename)
            return '/static/uploads/research_paper_feedback/' + filename
        else:
            return "Save File"

    @feedback_blueprint.route('/written_feedback_submit', methods=['GET', 'POST'])
    def written_feedback_submit():
        email = session['email']
        # print('Joining Email', email)
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """SELECT write_feedback_here, first_name, last_name FROM application_page WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchone()

        first_name = records['first_name']
        last_name = records['last_name']

        if request.method == 'POST':
            write_feedback_here = request.form['write_feedback_here']
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Fixed format for date
            current_time = datetime.datetime.now().strftime('%H:%M:%S')  # Fixed format for time

            # Handle case where joining_report is not already uploaded
            if not records.get('hra_utility_report'):
                update_query = """UPDATE application_page 
                                                  SET write_feedback_here=%s,
                                                  written_feedback_uploaded_date=%s, written_feedback_uploaded_time=%s 
                                                  WHERE email = %s
                                          """
                cursor.execute(update_query, (write_feedback_here, current_date, current_time, email))
                cnx.commit()

                cursor.close()
                cnx.close()

                session['assessment'] = True
                return redirect(url_for('feedback.feedback'))
            else:
                # Case where joining_report is already uploaded
                cursor.close()
                cnx.close()
                flash('Undertaking Report is Already Uploaded', 'Error')
                return "Undertaking report is already uploaded", 400
        else:
            cursor.close()
            cnx.close()
            return redirect(url_for('feedback.feedback'))  # Redirect for non-POST requests