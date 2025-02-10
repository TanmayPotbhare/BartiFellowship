import datetime
import requests
import os
from classes.caste import casteController
from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response, jsonify

from classes.university import universityController

section2_blueprint = Blueprint('section2', __name__)


def section2_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @section2_blueprint.route('/get_college_data_by_university', methods=['GET', 'POST'])
    def get_college_data_by_university():
        u_id = request.form.get('u_id')
        print(u_id)
        college_obj = universityController(host)
        college_name = college_obj.get_college_name(u_id)
        return jsonify(college_name)

    @section2_blueprint.route('/section2', methods=['GET', 'POST'])
    def section2():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        if session.get('show_flash_section1', True):  # Retrieve and clear the flag
            flash('Profile section has been successfully saved.', 'success')
            # set the flag to "False" to prevent the flash message from being diaplayed repetitively displayed
            session['show_flash_section1'] = False

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        university_data = universityController(host)
        university_names = university_data.get_all_university()

        cursor.execute("SELECT * FROM cities")
        cities = cursor.fetchall()

        # Check if a record already exists for this user
        cursor.execute("SELECT * FROM application_page WHERE email = %s", (email,))
        record = cursor.fetchone()

        cursor.execute(" SELECT * from districts ")
        districts = cursor.fetchall()

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

            if record['phd_registration_date']:
            # Convert the Date to standard Format 
                DoB = record['phd_registration_date'] 
                formatted_phd_reg_date = DoB.strftime('%d-%b-%Y')
            else:
                formatted_phd_reg_date = None
                     

            return render_template('CandidatePages/ApplicationForm/section2.html', record=record, university_data=university_names,
                                   finally_approved=finally_approved, user=user, photo=photo, signup_record=signup_record, districts=districts,
                                   formatted_phd_reg_date=formatted_phd_reg_date, cities=cities,
                                   title='Application Form (Qualification Details)')
        else:
            user = "Student"
            photo = '/static/assets/img/default_user.png'
            finally_approved = 'pending'

        cursor.execute("SELECT * FROM signup WHERE email = %s", (email,))
        signup_record = cursor.fetchone()

        return render_template('CandidatePages/ApplicationForm/section2.html', record=record, university_data=university_names,
                               finally_approved=finally_approved, user=user, photo=photo, signup_record=signup_record, districts=districts,
                               title='Application Form (Qualification Details)', cities=cities)

    @section2_blueprint.route('/section2_submit', methods=['GET', 'POST'])
    def section2_submit():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        email = session['email']
        print('email section 2:', email)
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        # Check if a record already exists for this user
        cursor.execute("SELECT section2 FROM application_page WHERE email = %s", (email,))
        record = cursor.fetchone()
        filled_section2 = record['section2']

        # Initialize an empty dictionary if no record is found
        # if record is None:
        #     record = {}

        if request.method == 'POST':
            ssc_passing_year = request.form['ssc_passing_year']
            stream = request.form['stream']
            ssc_school_name = request.form['ssc_school_name']
            ssc_attempts = request.form['ssc_attempts']
            ssc_total = request.form['ssc_total']
            ssc_percentage = request.form['ssc_percentage']

            hsc_passing_year = request.form['hsc_passing_year']
            hsc_stream = request.form['hsc_stream']
            hsc_school_name = request.form['hsc_school_name']
            hsc_attempts = request.form['hsc_attempts']
            hsc_total = request.form['hsc_total']
            hsc_percentage = request.form['hsc_percentage']

            graduation_passing_year = request.form['graduation_passing_year']
            grad_stream = request.form['grad_stream']
            graduation_school_name = request.form['graduation_school_name']
            grad_attempts = request.form['grad_attempts']
            grad_total = request.form['grad_total']
            graduation_percentage = request.form['graduation_percentage']

            phd_passing_year = request.form['phd_passing_year']
            pg_stream = request.form['pg_stream']
            phd_school_name = request.form['phd_school_name']
            pg_attempts = request.form['pg_attempts']
            pg_total = request.form['pg_total']
            phd_percentage = request.form['phd_percentage']

            qualified_exams = request.form.getlist('qualified_exams[]') 
            if qualified_exams:  # Check if any checkboxes were selected
                have_you_qualified = ','.join(qualified_exams) 
            else:
                have_you_qualified = None 

            have_you_qualified_other = request.form['have_you_qualified_other']
            phd_registration_date = request.form['phd_registration_date']
            fellowship_applying_year = request.form['fellowship_applying_year']
            phd_registration_day = request.form['phd_registration_day']
            phd_registration_month = request.form['phd_registration_month']
            phd_registration_year = request.form['phd_registration_year']
            phd_registration_age = request.form['phd_registration_age']

            concerned_university = request.form['concerned_university']
            other_university = request.form['other_university']
            name_of_college = request.form['name_of_college']
            other_college_name = request.form['other_college_name']
            department_name = request.form['department_name']
            topic_of_phd = request.form['topic_of_phd']
            name_of_guide = request.form['name_of_guide']
            faculty = request.form['faculty']
            other_faculty = request.form['other_faculty']
            research_center_district = request.form['research_center_district']

            section2 = 'filled'

            if filled_section2 != 'filled':
                # Save the form data to the database
                print('Inserting new record for:' + email)
                sql = """
                    UPDATE application_page 
                    SET 
                        ssc_passing_year = %s, ssc_percentage = %s, ssc_school_name = %s, ssc_stream = %s, ssc_attempts = %s, ssc_total = %s,
                        hsc_passing_year = %s, hsc_percentage = %s, hsc_school_name = %s, hsc_stream = %s, hsc_attempts = %s, hsc_total = %s,
                        graduation_passing_year = %s, graduation_percentage = %s, graduation_school_name = %s, grad_stream = %s, grad_attempts = %s, grad_total = %s,
                        phd_passing_year = %s, phd_percentage = %s, phd_school_name = %s, pg_stream = %s, pg_attempts = %s, pg_total = %s,
                        have_you_qualified = %s, have_you_qualified_other =  %s, phd_registration_date = %s, fellowship_application_year = %s, phd_registration_day = %s,
                        phd_registration_month = %s, phd_registration_year = %s, phd_registration_age = %s, concerned_university = %s,
                        other_university = %s, name_of_college = %s, other_college_name = %s, department_name = %s, topic_of_phd = %s,
                        name_of_guide = %s, faculty = %s, other_faculty = %s, research_center_district = %s, section2 = %s
                    WHERE email = %s
                """
                values = (
                    ssc_passing_year, ssc_percentage, ssc_school_name, stream, ssc_attempts, ssc_total,
                    hsc_passing_year, hsc_percentage, hsc_school_name, hsc_stream, hsc_attempts, hsc_total,
                    graduation_passing_year, graduation_percentage, graduation_school_name, grad_stream, grad_attempts,
                    grad_total,
                    phd_passing_year, phd_percentage, phd_school_name, pg_stream, pg_attempts, pg_total,
                    have_you_qualified, have_you_qualified_other, phd_registration_date, fellowship_applying_year, phd_registration_day,
                    phd_registration_month, phd_registration_year, phd_registration_age, concerned_university,
                    other_university, name_of_college, other_college_name, department_name, topic_of_phd,
                    name_of_guide, faculty, other_faculty, research_center_district, section2, email  # Include `email` to identify the record
                )

                cursor.execute(sql, values)
                cnx.commit()
                session['show_flashed_section2'] = True
                return redirect(url_for('section3.section3'))
                # Check if the user is approved for fellowship no matter the year to show the desired sidebar.
        print('I am here')
        return redirect(url_for('section2.section2'))
