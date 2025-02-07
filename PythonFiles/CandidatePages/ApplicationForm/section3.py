import datetime
import requests
import os
from classes.caste import casteController
from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response, jsonify

from classes.university import universityController

section3_blueprint = Blueprint('section3', __name__)


def section3_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @section3_blueprint.route('/get_talukas/<int:district_id>', methods=['GET'])
    def get_talukas(district_id):
        # Assuming you have a function to get talukas from the district ID
        caste_class = casteController(host)
        talukas = caste_class.get_taluka_from_district(district_id)
        return jsonify({'talukas': talukas})

    @section3_blueprint.route('/section3', methods=['GET', 'POST'])
    def section3():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        if session.get('show_flashed_section2', True):  # Retrieve and clear the flag
            flash('Qualification section has been successfully saved.', 'success')
            # set the flag to "False" to prevent the flash message from being diaplayed repetitively displayed
            session['show_flashed_section2'] = False

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        caste_class = casteController(host)
        validity = caste_class.get_all_caste_validity_auth()

        cursor.execute(" SELECT * from districts ")
        districts = cursor.fetchall()

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

            return render_template('CandidatePages/ApplicationForm/section3.html', record=record, districts=districts,
                                   finally_approved=finally_approved, user=user, photo=photo, signup_record=signup_record,
                                   title='Application Form (Certificate Details)', validity=validity)
        else:
            user = "Student"
            photo = '/static/assets/img/default_user.png'
            finally_approved = 'pending'

        cursor.execute("SELECT * FROM signup WHERE email = %s", (email,))
        signup_record = cursor.fetchone()

        return render_template('CandidatePages/ApplicationForm/section3.html', record=record, districts=districts,
                               finally_approved=finally_approved, user=user, photo=photo, signup_record=signup_record,
                               title='Application Form (Certificate Details)', validity=validity)

    @section3_blueprint.route('/section3_submit', methods=['GET', 'POST'])
    def section3_submit():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        # Check if a record already exists for this user
        cursor.execute("SELECT section3 FROM application_page WHERE email = %s", (email,))
        record = cursor.fetchone()
        filled_section3 = record['section3']
        # Initialize an empty dictionary if no record is found
        # if record is None:
        #     record = {}

        if request.method == 'POST':
            family_annual_income = request.form['family_annual_income']
            income_certificate_number = request.form['income_certificate_number']
            issuing_authority = request.form['issuing_authority']
            income_issuing_district = request.form['income_issuing_district']
            income_issuing_taluka = request.form['income_issuing_taluka']

            domicile = request.form['domicile']
            domicile_number = request.form['domicile_number']
            domicile_issuing_authority = request.form['domicile_issuing_authority']
            domicile_issuing_district = request.form['domicile_issuing_district']
            domicile_issuing_taluka = request.form['domicile_issuing_taluka']

            caste_certf = request.form['caste_certf']
            caste_certf_number = request.form['caste_certf_number']
            caste_issuing_authority = request.form['caste_issuing_authority']
            issuing_district = request.form['issuing_district']
            caste_issuing_taluka = request.form['caste_issuing_taluka']

            validity_certificate = request.form['validity_certificate']

            if validity_certificate == 'Yes':
                validity_cert_number = request.form['validity_cert_number'] 
                validity_issuing_authority = request.form['validity_issuing_authority'] 
                validity_issuing_district = request.form['validity_issuing_district'] 
                validity_issuing_taluka = request.form['validity_issuing_taluka'] 
            else: 
                validity_cert_number = '' 
                validity_issuing_authority = '' 
                validity_issuing_district = '' 
                validity_issuing_taluka = '' 

            section3 = 'filled'

            # print(request.form)

            if filled_section3 != 'filled':
                # Save the form data to the database
                print('Inserting new record for:' + email)
                sql = """
                    UPDATE application_page 
                    SET 
                        family_annual_income = %s, income_certificate_number = %s, issuing_authority = %s, income_issuing_district = %s, income_issuing_taluka = %s, 
                        domicile = %s, domicile_number = %s, domicile_issuing_authority = %s, domicile_issuing_district = %s, domicile_issuing_taluka = %s,
                        caste_certf = %s, caste_certf_number = %s, caste_issuing_authority = %s, issuing_district = %s, caste_issuing_taluka = %s,
                        validity_certificate = %s, validity_cert_number = %s, validity_issuing_authority = %s, validity_issuing_district = %s, validity_issuing_taluka = %s,
                        section3 = %s
                    WHERE email = %s
                """
                values = (
                    family_annual_income, income_certificate_number, issuing_authority, income_issuing_district, income_issuing_taluka,
                    domicile, domicile_number, domicile_issuing_authority, domicile_issuing_district, domicile_issuing_taluka,
                    caste_certf, caste_certf_number, caste_issuing_authority, issuing_district, caste_issuing_taluka,
                    validity_certificate, validity_cert_number, validity_issuing_authority, validity_issuing_district, validity_issuing_taluka,
                    section3, email  # Include `email` to identify the record
                )

                cursor.execute(sql, values)
                cnx.commit()
                session['show_flashed_section3'] = True
                return redirect(url_for('section4.section4'))
                # Check if the user is approved for fellowship no matter the year to show the desired sidebar.

        return redirect(url_for('section3.section3'))
