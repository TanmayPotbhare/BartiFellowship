import datetime
import requests
import os
from classes.caste import casteController
from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response, jsonify


section4_blueprint = Blueprint('section4', __name__)


def section4_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @section4_blueprint.route('/get_ifsc_data', methods=['GET'])
    def get_ifsc_data():
        ifsc = request.args.get('ifsc')
        api_url = f'https://ifsc.razorpay.com/{ifsc}'
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
            data = response.json()
            return jsonify(data)
        except requests.exceptions.RequestException as e:
            return jsonify({'error': str(e)}), 500

    @section4_blueprint.route('/section4', methods=['GET', 'POST'])
    def section4():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        if session.get('show_flashed_section3', True):  # Retrieve and clear the flag
            flash('Certificate Details section has been successfully saved.', 'success')
            # set the flag to "False" to prevent the flash message from being diaplayed repetitively displayed
            session['show_flashed_section3'] = False

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        caste_class = casteController(host)
        all_caste = caste_class.get_all_caste_details()

        # Check if a record already exists for this user
        cursor.execute("SELECT * FROM application_page WHERE email = %s", (email,))
        record = cursor.fetchone()

        if record:
            # print(record)
            if record['final_approval'] not in ['accepted', 'None', '']:
                finally_approved = 'pending'
            else:
                finally_approved = 'approved'

            if record:
                user = record['first_name'] + ' ' + record['last_name']
                photo = record['applicant_photo']
            else:
                user = "Admin"
                photo = '/static/assets/img/default_user.png'

            signup_record = record['email']

            return render_template('CandidatePages/ApplicationForm/section4.html', record=record, all_caste=all_caste,
                                   finally_approved=finally_approved, user=user, photo=photo, signup_record=signup_record,
                                   title='Application Form (Bank Details)')
        else:
            user = "Student"
            finally_approved = 'pending'

            cursor.execute("SELECT * FROM signup WHERE email = %s", (email,))
            signup_record = cursor.fetchone()

        return render_template('CandidatePages/ApplicationForm/section4.html', record=record, all_caste=all_caste,
                               finally_approved=finally_approved, user=user, signup_record=signup_record,
                               title='Application Form (Bank Details)')

    @section4_blueprint.route('/section4_submit', methods=['GET', 'POST'])
    def section4_submit():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        # Check if a record already exists for this user
        cursor.execute("""
            SELECT section4 FROM application_page WHERE email = %s
        """, (email,))
        record = cursor.fetchone()
        filled_section4 = record['section4']
        # Initialize an empty dictionary if no record is found
        # if record is None:
        #     record = {}

        if request.method == 'POST':
            salaried = request.form['salaried']
            disability = request.form['disability']
            type_of_disability = request.form['type_of_disability']
            perc_of_disability = request.form['perc_of_disability']
            father_name = request.form['father_name']
            mother_name = request.form['mother_name']
            work_in_government = request.form['work_in_government']

            no_of_gov_employee = request.form['no_of_gov_employee']

            emp1_name = request.form['emp1_name']
            emp1_position = request.form['emp1_position']
            emp1_relation = request.form['emp1_relation']

            emp2_name = request.form['emp2_name']
            emp2_position = request.form['emp2_position']
            emp2_relation = request.form['emp2_relation']

            emp3_name = request.form['emp3_name']
            emp3_position = request.form['emp3_position']
            emp3_relation = request.form['emp3_relation']

            bank_name = request.form['bank_name']
            account_number = request.form['account_number']
            ifsc_code = request.form['ifsc_code']
            account_holder_name = request.form['account_holder_name']
            micr = request.form['micr']
            section4 = 'filled'

            if filled_section4 != 'filled':
                # Save the form data to the database
                sql = """
                        UPDATE application_page
                        SET
                            salaried = %s, disability = %s, type_of_disability = %s, disability_percentage= %s,
                            father_name = %s, mother_name = %s, work_in_government = %s, no_of_gov_employee = %s,
                            emp1_name =  %s, emp1_position = %s, emp1_relation = %s,
                            emp2_name =  %s, emp2_position = %s, emp2_relation = %s,
                            emp3_name =  %s, emp3_position = %s, emp3_relation = %s,
                            bank_name = %s,account_number = %s,ifsc_code = %s, account_holder_name = %s, micr = %s, section4 = %s
                        WHERE email = %s
                    """
                values = (
                    salaried, disability, type_of_disability, perc_of_disability,
                    father_name, mother_name, work_in_government, no_of_gov_employee,
                    emp1_name, emp1_position, emp1_relation,
                    emp2_name, emp2_position, emp2_relation,
                    emp3_name, emp3_position, emp3_relation,
                    bank_name, account_number, ifsc_code, account_holder_name, micr, section4, email
                )

                cursor.execute(sql, values)
                cnx.commit()
                session['show_flashed_section4'] = True
                return redirect(url_for('section5.section5'))
                # Check if the user is approved for fellowship no matter the year to show the desired sidebar.
        else:
            return redirect(url_for('section4.section4'))
