import datetime
import requests
import os
from Classes.caste import casteController
from Classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response, jsonify


section1_blueprint = Blueprint('section1', __name__)


def section1_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)

    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @section1_blueprint.route('/app_form_info')
    def app_form_info():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))
        return render_template('CandidatePages/app_form_info.html')

    @section1_blueprint.route('/get_pincode_data', methods=['GET'])
    def get_pincode_data():
        pincode_data = request.args.get('pincode')
        api_url = f'https://api.worldpostallocations.com/pincode?postalcode={pincode_data}&countrycode=IN'
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
            data = response.json()
            return jsonify(data)
        except requests.exceptions.RequestException as e:
            return jsonify({'error': str(e)}), 500

    @section1_blueprint.route('/get_subcastes/<int:unique_number>', methods=['GET'])
    def get_subcastes(unique_number):
        caste_class = casteController(host)
        subcastes = caste_class.get_subcastes_by_unique_number(unique_number)
        return jsonify({'subcastes': subcastes})

    @section1_blueprint.route('/section1', methods=['GET', 'POST'])
    def section1():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        caste_class = casteController(host)
        all_caste = caste_class.get_all_caste_details()
        # print(all_caste)

        # Check if a record already exists for this user
        cursor.execute("SELECT * FROM application_page WHERE email = %s", (email,))
        record = cursor.fetchone()

        cursor.execute("SELECT * FROM signup WHERE email = %s", (email,))
        signup = cursor.fetchone()
        # print(record)
        # if record:
        #     print("My Caste is : " + record)

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

            # Convert the Date to standard Format
            DoB = record['date_of_birth'] 
            formatted_date_of_birth = DoB.strftime('%d-%b-%Y')

            return render_template('CandidatePages/ApplicationForm/section1.html', record=record, all_caste=all_caste,
                                   finally_approved=finally_approved, user=user, photo=photo, signup_record=signup_record,
                                   formatted_date_of_birth=formatted_date_of_birth, signup=signup,
                                   title='Application Form (Personal Details)')
        else:
            user = signup['first_name'] + ' ' + signup['last_name']
            photo = '/static/assets/img/default_user.png'
            finally_approved = 'pending'
            
            if record:
                application_form_status = record['section5']
            else:
               application_form_status = "Not filled"

            cursor.execute("SELECT * FROM signup WHERE email = %s", (email,))
            signup_record = cursor.fetchone()

        return render_template('CandidatePages/ApplicationForm/section1.html', record=record, all_caste=all_caste,
                               finally_approved=finally_approved, user=user, photo=photo, signup_record=signup_record,
                               application_form_status=application_form_status, signup=signup,
                               title='Application Form (Personal Details)')

    @section1_blueprint.route('/section1_submit', methods=['GET', 'POST'])
    def section1_submit():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        # Check if a record already exists for this user
        cursor.execute("SELECT applicant_photo, adhaar_number, adhaar_seeding, first_name, final_approval,"
                       "middle_name, last_name, mobile_number, email, date_of_birth, gender, age, caste, your_caste, subcaste,"
                       "pvtg, pvtg_caste, marital_status, same_address, add_1, add_2, pincode, village, other_village, taluka, district, state, city"
                       " FROM application_page WHERE email = %s", (email,))
        record = cursor.fetchone()
        # print(record)

        # Initialize an empty dictionary if no record is found
        if record is None:
            record = {}

        if request.method == 'POST':
            photo = request.files['applicant_photo']
            adhaar_number = request.form['adhaar_number']
            adhaar_seeding = request.files['adhaar_seeding_bank']
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            last_name = request.form['last_name']
            mobile_number = request.form['mobile_number']
            email = session['email']
            date_of_birth = request.form['date_of_birth']
            gender = request.form['gender']
            age = request.form['age']
            caste = request.form['caste']
            # pvtg = request.form['pvtg']
            # pvtg_caste = request.form['pvtg_caste']
            your_caste = request.form['your_caste']
            # subcaste = request.form['subcaste']
            marital_status = request.form['marital_status']
            add_1 = request.form['add_1']
            pincode = request.form['pincode']
            village = request.form['village']
            other_village = request.form['other_village']
            taluka = request.form['taluka']
            district = request.form['district']
            state = request.form['state']
            same_address = request.form['same_address']
            comm_add_1 = request.form['comm_add_1']
            comm_pincode = request.form['comm_pincode']
            comm_village = request.form['comm_village']
            comm_other_village = request.form['comm_other_village']
            comm_taluka = request.form['comm_taluka']
            comm_district = request.form['comm_district']
            comm_state = request.form['comm_state']
            section1 = 'filled'
            # print("My Caste is : " + your_caste)

            # Handle file upload (applicant's photo)
            photo_path = save_applicant_photo(photo, first_name, last_name)
            adhaar_path = save_applicant_photo(adhaar_seeding, first_name, last_name)

            if is_adhaar_already_exist(adhaar_number):
                flash('The Aadhaar number you entered is already registered. Please use a different Aadhaar number or log in if you have an account.', 'info')
                return redirect(url_for('section1.section1'))

            if not record:
                # Save the form data to the database
                sql = """
                INSERT INTO application_page (
                    applicant_photo, adhaar_number, adhaar_seeding_doc, first_name, middle_name, last_name, 
                    mobile_number, email, date_of_birth, gender, age, caste, your_caste, 
                    marital_status, add_1, pincode, village, other_village, taluka, district, state, same_address,
                    comm_add_1, comm_pincode, comm_village, comm_other_village, comm_taluka, comm_district, comm_state, section1
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
                """

                values = (
                    photo_path, adhaar_number, adhaar_path, first_name, middle_name, last_name,
                    mobile_number, email, date_of_birth, gender, age, caste, your_caste,
                    marital_status, add_1, pincode, village, other_village, taluka, district, state, same_address,
                    comm_add_1, comm_pincode, comm_village, comm_other_village, comm_taluka, comm_district, comm_state, section1
                )

                cursor.execute(sql, values)
                cnx.commit()
                session['show_flash_section1'] = True
                return redirect(url_for('section2.section2'))
                # Check if the user is approved for fellowship no matter the year to show the desired sidebar.
        else:
            return redirect(url_for('section1.section1'))

    def save_applicant_photo(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['UPLOAD_PHOTO_SECTION1'], filename))
            # return os.path.join(app.config['UPLOAD_PHOTO_SECTION1'], filename)
            return '/static/uploads/image_retrive/' + filename
        else:
            return "Save File"

    # ---------------------------- Check if User is already Registered ---------------------
    def is_adhaar_already_exist(adhaar_number):  # ---------------- CHECK IF EMAIL IS IN THE DATABASE
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect()
        sql = "SELECT adhaar_number FROM application_page WHERE adhaar_number = %s"
        cursor.execute(sql, (adhaar_number,))
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        return result
