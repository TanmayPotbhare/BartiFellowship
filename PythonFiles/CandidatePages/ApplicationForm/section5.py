from datetime import datetime
import requests
import os
from classes.caste import casteController
from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response, jsonify

from classes.university import universityController

section5_blueprint = Blueprint('section5', __name__)


def section5_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @section5_blueprint.route('/get_talukas/<int:district_id>', methods=['GET'])
    def get_talukas(district_id):
        # Assuming you have a function to get talukas from the district ID
        caste_class = casteController(host)
        talukas = caste_class.get_taluka_from_district(district_id)
        return jsonify({'talukas': talukas})

    @section5_blueprint.route('/section5', methods=['GET', 'POST'])
    def section5():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        if session.get('show_flashed_section4', True):  # Retrieve and clear the flag
            flash('Bank Details section has been successfully saved.', 'success')
            # set the flag to "False" to prevent the flash message from being diaplayed repetitively displayed
            session['show_flashed_section4'] = False 
            
        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

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

            return render_template('CandidatePages/ApplicationForm/section5.html', record=record,
                                   finally_approved=finally_approved, user=user, photo=photo, signup_record=signup_record,
                                   title='Application Form (Upload Documents)')
        else:
            user = "Student"
            photo = '/static/assets/img/default_user.png'
            finally_approved = 'pending'

        cursor.execute("SELECT * FROM signup WHERE email = %s", (email,))
        signup_record = cursor.fetchone()

        return render_template('CandidatePages/ApplicationForm/section5.html', record=record,
                               finally_approved=finally_approved, user=user, photo=photo, signup_record=signup_record,
                               title='Application Form (Upload Documents)')

    # @section5_blueprint.route('/section5_submit', methods=['GET', 'POST'])
    # def section5_submit():
    #     if not session.get('logged_in_from_login'):
    #         # Redirect to the admin login page if the user is not logged in
    #         return redirect(url_for('login_signup.login'))

    #     email = session['email']
    #     # print('I am here', email)
    #     host = HostConfig.host
    #     connect_param = ConnectParam(host)
    #     cnx, cursor = connect_param.connect(use_dict=True)

    #     # Check if a record already exists for this user
    #     cursor.execute("SELECT first_name, last_name, section5 FROM application_page WHERE email = %s", (email,))
    #     record = cursor.fetchone()
    #     filled_section5 = record['section5']

    #     first_name = record['first_name']
    #     last_name = record['last_name']

    #     if request.method == 'POST':
    #         print('Got a Post Request')

    #         # Handling file uploads
    #         file_fields = [
    #             'signature', 'adhaar_card_doc', 'pan_card_doc', 'domicile_doc', 'caste_doc', 'validity_doc',
    #             'income_doc',
    #             'ssc_doc', 'hsc_doc', 'grad_doc', 'post_grad_doc', 'entrance_doc', 'phd_reciept_doc',
    #             'guideAllotment_doc',
    #             'guideAccept_doc', 'rac_doc', 'confirmation_doc', 'joining_doc', 'annexureA_doc', 'annexureB_doc',
    #             'annexureC_doc', 'annexureD_doc', 'disable_doc', 'gazete_doc', 'selfWritten_doc', 'research_letter_doc'
    #         ]

    #         uploaded_files = {}

    #         for field in file_fields:
    #             uploaded_files[field] = applicant_pdf_upload_section_five(request.files.get(field), first_name,
    #                                                                       last_name)

    #         # Extract all uploaded files from the dictionary
    #         signature = uploaded_files['signature']
    #         adhaar_card_doc = uploaded_files['adhaar_card_doc']
    #         pan_card_doc = uploaded_files['pan_card_doc']
    #         domicile_doc = uploaded_files['domicile_doc']
    #         caste_doc = uploaded_files['caste_doc']
    #         validity_doc = uploaded_files['validity_doc']
    #         income_doc = uploaded_files['income_doc']
    #         ssc_doc = uploaded_files['ssc_doc']
    #         hsc_doc = uploaded_files['hsc_doc']
    #         grad_doc = uploaded_files['grad_doc']
    #         post_grad_doc = uploaded_files['post_grad_doc']
    #         entrance_doc = uploaded_files['entrance_doc']
    #         phd_reciept_doc = uploaded_files['phd_reciept_doc']
    #         guideAllotment_doc = uploaded_files['guideAllotment_doc']
    #         guideAccept_doc = uploaded_files['guideAccept_doc']
    #         rac_doc = uploaded_files['rac_doc']
    #         confirmation_doc = uploaded_files['confirmation_doc']
    #         joining_doc = uploaded_files['joining_doc']
    #         annexureA_doc = uploaded_files['annexureA_doc']
    #         annexureB_doc = uploaded_files['annexureB_doc']
    #         annexureC_doc = uploaded_files['annexureC_doc']
    #         annexureD_doc = uploaded_files['annexureD_doc']
    #         disable_doc = uploaded_files['disable_doc']
    #         gazete_doc = uploaded_files['gazete_doc']
    #         selfWritten_doc = uploaded_files['selfWritten_doc']
    #         research_letter_doc = uploaded_files['research_letter_doc']

    #         section5 = 'filled'
    #         lock_application_status = 'locked'

    #         if filled_section5 != 'filled':
    #             print('No Records just insert')
    #             # Save the form data to the database
    #             print('Inserting new record for:' + email)
    #             sql = """
    #                 UPDATE application_page 
    #                 SET 
    #                     signature = %s, adhaar_card_doc = %s, pan_card_doc = %s, domicile_doc = %s, 
    #                     caste_doc = %s, validity_doc = %s, income_doc = %s, ssc_doc = %s, hsc_doc = %s,
    #                     grad_doc = %s, post_grad_doc = %s, entrance_doc = %s, phd_reciept_doc = %s, 
    #                     guideAllotment_doc = %s, guideAccept_doc = %s, rac_doc = %s, confirmation_doc = %s, 
    #                     joining_doc = %s, annexureA_doc = %s, annexureB_doc = %s, annexureC_doc = %s, 
    #                     annexureD_doc = %s, disable_doc = %s, gazete_doc = %s, selfWritten_doc = %s,
    #                     research_letter_doc = %s, section5 = %s, lock_application_form  = %s
    #                 WHERE email = %s
    #             """
    #             values = (
    #                 signature, adhaar_card_doc, pan_card_doc, domicile_doc, caste_doc, validity_doc, income_doc,
    #                 ssc_doc, hsc_doc, grad_doc, post_grad_doc, entrance_doc, phd_reciept_doc, guideAllotment_doc,
    #                 guideAccept_doc, rac_doc, confirmation_doc, joining_doc, annexureA_doc, annexureB_doc, 
    #                 annexureC_doc, annexureD_doc, disable_doc, gazete_doc, selfWritten_doc, research_letter_doc,
    #                 section5, lock_application_status, email  # Include `email` to identify the record
    #             )

    #             cursor.execute(sql, values)
    #             cnx.commit()

    #             cursor.execute("SELECT first_name, last_name, email, user, year FROM signup WHERE email = %s",
    #                            (email,))
    #             old_user = cursor.fetchone()
    #             cnx.commit()

    #             print(old_user)

    #             year_check = str(old_user['year'])
    #             print(year_check)
    #             user_check = old_user['user']

    #             if year_check in ['2021', '2022'] and user_check == 'Old User':
    #                 print('Updating Old User Record')
    #                 # Enter Old User Applicant ID
    #                 enter_old_applicant_id(email)
    #                 # Enter Old Presenty Record
    #                 enter_presenty_record(email)
    #                 insert_payment_sheet_record(email)
    #             else:
    #                 print('email', email)
    #                 # Inserts three differnet flags with applicant ID.
    #                 enter_applicant_id(email)
    #                 # Checks the email in Presenty and if not inserts it.
    #                 enter_presenty_record(email)

    #             # Send Email of Completion
    #             # send_email_of_completion(email)
    #             return redirect(url_for('section5.completed_application'))
    #             # Check if the user is approved for fellowship no matter the year to show the desired sidebar.
    #         else:
    #             return redirect(url_for('section5.section5'))
    #     else:
    #         # Handle GET request (display empty form, or previously filled data if necessary)
    #         return redirect(url_for('section5.section5'))

    @section5_blueprint.route('/section5_submit', methods=['GET', 'POST'])
    def section5_submit():
        if not session.get('logged_in_from_login'):
            return redirect(url_for('login_signup.login'))

        email = session['email']
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        # Fetch existing record
        cursor.execute("SELECT * FROM application_page WHERE email = %s", (email,))
        record = cursor.fetchone()
        filled_section5 = record['section5']

        first_name = record['first_name']
        last_name = record['last_name']

        if request.method == 'POST':
            print('Got a Post Request')

            # List of all file fields
            file_fields = [
                'signature', 'adhaar_card_doc', 'pan_card_doc', 'domicile_doc', 'caste_doc', 'validity_doc',
                'income_doc', 'ssc_doc', 'hsc_doc', 'grad_doc', 'post_grad_doc', 'entrance_doc', 'phd_reciept_doc',
                'guideAllotment_doc', 'guideAccept_doc', 'rac_doc', 'confirmation_doc', 'joining_doc',
                'annexureA_doc', 'annexureB_doc', 'annexureC_doc', 'annexureD_doc', 'disable_doc', 'gazete_doc',
                'selfWritten_doc', 'research_letter_doc'
            ]

            uploaded_files = {}

            for field in file_fields:
                file = request.files.get(field)
                if file and file.filename:
                    # New file uploaded
                    uploaded_files[field] = applicant_pdf_upload_section_five(file, first_name, last_name)
                else:
                    # Use existing file from DB
                    uploaded_files[field] = record[field]

            # Status fields
            section5 = 'filled'
            lock_application_status = 'locked'

            print('Updating or inserting data for:', email)
            sql = """
                UPDATE application_page 
                SET 
                    signature = %s, adhaar_card_doc = %s, pan_card_doc = %s, domicile_doc = %s, caste_doc = %s, validity_doc = %s, income_doc = %s, ssc_doc = %s,
                    hsc_doc = %s, grad_doc = %s, post_grad_doc = %s, entrance_doc = %s, phd_reciept_doc = %s, guideAllotment_doc = %s, guideAccept_doc = %s, 
                    rac_doc = %s, confirmation_doc = %s, joining_doc = %s, annexureA_doc = %s, annexureB_doc = %s, annexureC_doc = %s, annexureD_doc = %s, 
                    disable_doc = %s, gazete_doc = %s, selfWritten_doc = %s, research_letter_doc = %s, section5 = %s, lock_application_form = %s
                WHERE email = %s
            """

            values = (
                uploaded_files['signature'],
                uploaded_files['adhaar_card_doc'],
                uploaded_files['pan_card_doc'],
                uploaded_files['domicile_doc'],
                uploaded_files['caste_doc'],
                uploaded_files['validity_doc'],
                uploaded_files['income_doc'],
                uploaded_files['ssc_doc'],
                uploaded_files['hsc_doc'],
                uploaded_files['grad_doc'],
                uploaded_files['post_grad_doc'],
                uploaded_files['entrance_doc'],
                uploaded_files['phd_reciept_doc'],
                uploaded_files['guideAllotment_doc'],
                uploaded_files['guideAccept_doc'],
                uploaded_files['rac_doc'],
                uploaded_files['confirmation_doc'],
                uploaded_files['joining_doc'],
                uploaded_files['annexureA_doc'],
                uploaded_files['annexureB_doc'],
                uploaded_files['annexureC_doc'],
                uploaded_files['annexureD_doc'],
                uploaded_files['disable_doc'],
                uploaded_files['gazete_doc'],
                uploaded_files['selfWritten_doc'],
                uploaded_files['research_letter_doc'],
                section5,
                lock_application_status,
                email
            )

            cursor.execute(sql, values)
            cnx.commit()

            # Only do these actions on first fill (not for updates)
            if filled_section5 != 'filled':
                cursor.execute("SELECT first_name, last_name, email, user, year FROM signup WHERE email = %s", (email,))
                old_user = cursor.fetchone()

                year_check = str(old_user['year'])
                user_check = old_user['user']

                if year_check in ['2021', '2022'] and user_check == 'Old User':
                    print('Updating Old User Record')
                    enter_old_applicant_id(email)
                    enter_presenty_record(email)
                    insert_payment_sheet_record(email)
                else:
                    enter_applicant_id(email)
                    enter_presenty_record(email)

            # Optional: send_email_of_completion(email)

            flash('Document Section submitted successfully and the Application form is locked.', 'success')
            return redirect(url_for('section5.completed_application'))

        else:
            return redirect(url_for('section5.section5'))

    def applicant_pdf_upload_section_five(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['USER_DOC_SEC_FIVE'], filename))
            # return os.path.join(app.config['USER_DOC_SEC_FIVE'], filename)
            return '/static/uploads/user_doc_secfive/' + filename
        else:
            return "Save File"

    import datetime

    def enter_applicant_id(email):
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute("SELECT id, fellowship_application_year FROM application_page WHERE email = %s", (email,))
        applicant = cursor.fetchone()

        if applicant:  # Check if applicant is found
            unique_id = applicant['id']
            year = applicant['fellowship_application_year']

            applicant_id = 'BARTI' + '/' + 'BANRF' + '/' + str(year) + '/' + str(unique_id)
            form_filled = '1'
            application_form_status = 'submitted'
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.datetime.now().strftime('%H:%M:%S')

            sql = """
                UPDATE application_page 
                SET 
                    applicant_id = %s, form_filled = %s, application_form_status = %s, application_date = %s, 
                    application_time = %s
                WHERE email = %s
            """
            values = (applicant_id, form_filled, application_form_status, current_date, current_time, email)

            cursor.execute(sql, values)
            cnx.commit()
            return 'Applicant ID inserted successfully'
        else:
            return 'Applicant not found'

    def enter_old_applicant_id(email):
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute("SELECT id, fellowship_application_year FROM application_page WHERE email = %s", (email,))
        applicant = cursor.fetchone()

        if applicant:  # Check if applicant is found
            unique_id = applicant['id']
            year = applicant['fellowship_application_year']

            applicant_id = 'BARTI' + '/' + 'BANRF' + '/' + str(year) + '/' + str(unique_id)
            form_filled = '1'
            application_form_status = 'submitted'
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.datetime.now().strftime('%H:%M:%S')

            status = 'accepted'
            scrutiny_status = 'accepted'
            final_approval = 'accepted'
            approved_for = year
            final_approval_day = datetime.datetime.now().strftime('%d')
            final_approval_month = datetime.datetime.now().strftime('%m')
            final_approval_year = year

            sql = """
                UPDATE application_page 
                SET 
                    applicant_id = %s, form_filled = %s, application_form_status = %s, application_date = %s, 
                    application_time = %s, status = %s, scrutiny_status = %s, final_approval = %s, final_approved_date = %s, 
                    final_approval_day = %s, final_approval_month = %s, final_approval_year = %s, approved_for = %s
                WHERE email = %s
            """
            values = (applicant_id, form_filled, application_form_status, current_date, current_time,
                      status, scrutiny_status, final_approval, current_date, final_approval_day, final_approval_month,
                      final_approval_year, approved_for, email)

            cursor.execute(sql, values)
            cnx.commit()
            return 'Applicant ID inserted successfully'
        else:
            return 'Applicant not found'

    def enter_presenty_record(email):
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d')

        # Check if a record already exists for this user
        cursor.execute("SELECT * FROM award_letter WHERE email = %s", (email,))
        presenty = cursor.fetchone()

        if presenty and presenty['email'] == email:
            return 'Email already in Presenty records'
        else:
            # Insert the email into the table if not present
            sql = "INSERT INTO award_letter (email, submission_date) VALUES (%s, %s)"
            values = (email, current_datetime)
            cursor.execute(sql, values)
            cnx.commit()
            return 'Email added to Presenty records'

    def send_email_of_completion(email):
        return True

    @section5_blueprint.route('/completed_application')
    def completed_application():
        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

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

        return render_template('CandidatePages/ApplicationForm/completed_application.html', record=record,
                               finally_approved=finally_approved, user=user, photo=photo, signup_record=signup_record)


    # @section5_blueprint.route('/load_pament_data')
    # def load_pament_data():
    #     host = HostConfig.host
    #     connect_param = ConnectParam(host)
    #     cnx, cursor = connect_param.connect(use_dict=True)
    #
    #     cursor.execute("SELECT * FROM application_page WHERE form_filled = '1' AND application_form_status = 'submitted' ")
    #     result = cursor.fetchall()
    #
    #
    #     for row in result:
    #         email = row['email']
    #         insert_payment_sheet_record(email)
    #
    #     return render_template('test_pdf.html', result=result)

    def insert_payment_sheet_record(email):
        """
        This function is also written in Section5.py for Old Users as they are already accepted.
        Here it is for new users.
        """
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        payment_records = []

        cursor.execute("SELECT * FROM application_page WHERE email = %s", (email,))
        result = cursor.fetchone()
        # print('Student Record:', result)

        cursor.execute("SELECT city, code FROM cities where city=%s", (result['research_center_district'],))
        city_rates = cursor.fetchone()
        # print('City and Code:', city_rates)

        cursor.execute("SELECT * FROM hra_rate_master")
        master = cursor.fetchall()
        # print('Rate Master:', master)

        if result and master:
            # -----------------------------------------
            # These are the fields for Payment sheet in order

            fullname = result['first_name'] + ' ' + result['middle_name'] + ' ' + result['last_name']
            email = result['email']
            fellowship_awarded = result['fellowship_awarded_date']
            fellowship_awarded_year = result['fellowship_application_year']
            faculty = result['faculty']
            date = result['phd_registration_date']
            total_months = 6
            disability = result['disability']
            bank_name = result['bank_name']
            ifsc_code = result['ifsc_code']
            account_number = result['account_number']

            current_date = datetime.datetime.now().strftime('%Y-%m-%d')
            start_date = result['phd_registration_date']

            fellowship_durations = {}
            current_quarter_start = start_date

            for i in range(10):  # 10 quarters of 6 months each
                quarter_start = current_quarter_start  # Use the current quarter's start date
                quarter_end = quarter_start + datetime.timedelta(days=6 * 30)

                quarter_start_str = quarter_start.strftime('%Y-%m-%d')
                quarter_end_str = quarter_end.strftime('%Y-%m-%d')

                if i < 9:  # Check if it's not the last quarter
                    current_quarter_start = quarter_end + datetime.timedelta(days=1)  # Update for the next quarter

                if i < 4:  # First two years (4 quarters)
                    fellowship_type = "jrf_" + str((i // 2) + 1)  # jrf_1 and jrf_2
                else:  # Next three years (6 quarters)
                    fellowship_type = "srf_" + str(((i - 4) // 2) + 1)  # Corrected logic here!

                fellowship_durations[fellowship_type + "_q" + str(i + 1)] = {"start": quarter_start_str,
                                                                             "end": quarter_end_str,
                                                                             "total_months": total_months}

                applicable_master = None
                fellowship_jrf_srf = fellowship_type
                for record in master:
                    master_fellowship_type = record['jrf_srf']
                    date_criteria = record['date_criteria']
                    less_greater_than = record['less_greater_than']

                    if master_fellowship_type == fellowship_jrf_srf:
                        if less_greater_than == 'less_than' and quarter_start < date_criteria:
                            applicable_master = record
                        elif less_greater_than == 'greater_than' and quarter_start >= date_criteria:
                            applicable_master = record

                if applicable_master:
                    fellowship = applicable_master['fellowship_amount']
                    jrf_srf = applicable_master['jrf_srf']

                    if city_rates['code'] == 'X':
                        hra_rate = applicable_master['X_rate']
                    elif city_rates['code'] == 'Y':
                        hra_rate = applicable_master['Y_rate']
                    elif city_rates['code'] == 'Z':
                        hra_rate = applicable_master['Z_rate']
                    else:
                        hra_rate = 0

                    if (i + 1) % 2 == 0:
                        if faculty == 'Arts':
                            contingency = applicable_master['contingency_other']
                        elif faculty == 'Law':
                            contingency = applicable_master['contingency_other']
                        elif faculty == 'Commerce':
                            contingency = applicable_master['contingency_other']
                        elif faculty == 'Other':
                            contingency = applicable_master['contingency_other']
                        elif faculty == 'Agriculture':
                            contingency = applicable_master['contingency_other']
                        elif faculty == 'Vocational':
                            contingency = applicable_master['contingency_other']
                        elif faculty == 'Science':
                            contingency = applicable_master['contingency_science']
                        else:
                            contingency = 0
                    else:
                        contingency = 0

                    if disability == 'Yes':
                        pwd = applicable_master['disability']
                        total_pwd = int(pwd) * int(total_months)
                    elif disability == 'No':
                        total_pwd = 0
                    else:
                        total_pwd = 0

                    # pprint(f"Quarter: {i + 1}, Fellowship Type: {fellowship_type}, Start Date: {quarter_start_str}, "
                    #       f"End Date: {quarter_end_str}, HRA Rate: {hra_rate}, Contingency: {contingency},"
                    #         f"Fellowship Amount: {fellowship}, JRF-SRF: {jrf_srf}, pwd: {total_pwd}")

                    total_fellowship =  int(fellowship) * int(total_months)
                    convert_rate = (float(hra_rate) / 100)
                    hra_amount = convert_rate * int(fellowship)
                    total_hra = int(hra_amount) * int(total_months)
                    duration_date_from = quarter_start_str
                    duration_date_to = quarter_end_str
                    applicant_id = result['applicant_id']

                final_result = {
                    'fullname': fullname,
                    'email': email,
                    'applicant_id': applicant_id,
                    'jrf_srf': jrf_srf,
                    'fellowship_awarded_date': fellowship_awarded,
                    'fellowship_awarded_year': fellowship_awarded_year,
                    'faculty': faculty,
                    'date': date,
                    'duration_date_from': duration_date_from,
                    'duration_date_to': duration_date_to,
                    'total_months': total_months,
                    'fellowship': fellowship,
                    'total_fellowship': total_fellowship,
                    'hra_rate': hra_rate,
                    'hra_amount': hra_amount,
                    'hra_months': total_months,
                    'total_hra_rate': total_hra,
                    'contingency': contingency,
                    'pwd': total_pwd,
                    'total': int(total_fellowship) + int(total_hra),
                    'city': city_rates['city'],
                    'bank_name': bank_name,
                    'ifsc_code': ifsc_code,
                    'account_number': account_number,
                    'quarters': 'Quarter ' + str(i + 1)
                }

                # pprint(final_result)

                fellowship_application_year = result['fellowship_application_year']
                application_year = fellowship_application_year
                table_name = f"payment_sheet_{application_year}"
                # print(table_name)

                # Construct the SQL Insert query with placeholders for 10 records
                insert_query = f"""
                    INSERT INTO {table_name} (
                        applicant_id, full_name, email, jrf_srf, fellowship_awarded_date, fellowship_awarded_year,
                        faculty, date, duration_date_from, duration_date_to, total_months, fellowship, 
                        total_fellowship, hra_rate, hra_amount, hra_months, total_hra_rate, contingency, 
                        pwd, total, city, bank_name, ifsc_code, account_number, quarters
                    )
                    VALUES 
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s);
                """

                values = [
                    final_result['applicant_id'],
                    final_result['fullname'], final_result['email'], final_result['jrf_srf'],
                    final_result['fellowship_awarded_date'],
                    final_result['fellowship_awarded_year'], final_result['faculty'], final_result['date'],
                    final_result['duration_date_from'],
                    final_result['duration_date_to'], final_result['total_months'], final_result['fellowship'],
                    final_result['total_fellowship'],
                    final_result['hra_rate'], final_result['hra_amount'], final_result['hra_months'],
                    final_result['total_hra_rate'],
                    final_result['contingency'], final_result['pwd'], final_result['total'],
                    final_result['city'], final_result['bank_name'],
                    final_result['ifsc_code'], final_result['account_number'], final_result['quarters']
                ]  # Repeat the values for all 10 quarters

                # Execute the query using your database connection
                cursor.execute(insert_query, values)

            cnx.commit()
            return flash('Application form locked and submitted successfully', 'success')
        else:
            error = flash('No record Found', 'error')
            return error