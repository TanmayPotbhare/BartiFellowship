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

    @section5_blueprint.route('/section5_submit', methods=['GET', 'POST'])
    def section5_submit():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        email = session['email']
        # print('I am here', email)
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        # Check if a record already exists for this user
        cursor.execute("SELECT first_name, last_name, section5 FROM application_page WHERE email = %s", (email,))
        record = cursor.fetchone()
        filled_section5 = record['section5']

        first_name = record['first_name']
        last_name = record['last_name']

        if request.method == 'POST':
            print('Got a Post Request')

            # Handling file uploads
            file_fields = [
                'signature', 'adhaar_card_doc', 'pan_card_doc', 'domicile_doc', 'caste_doc', 'validity_doc',
                'income_doc',
                'ssc_doc', 'hsc_doc', 'grad_doc', 'post_grad_doc', 'entrance_doc', 'phd_reciept_doc',
                'guideAllotment_doc',
                'guideAccept_doc', 'rac_doc', 'confirmation_doc', 'joining_doc', 'annexureAC_doc', 'annexureB_doc',
                'disable_doc', 'gazete_doc', 'selfWritten_doc', 'research_letter_doc'
            ]

            uploaded_files = {}

            for field in file_fields:
                uploaded_files[field] = applicant_pdf_upload_section_five(request.files.get(field), first_name,
                                                                          last_name)

            # Extract all uploaded files from the dictionary
            signature = uploaded_files['signature']
            adhaar_card_doc = uploaded_files['adhaar_card_doc']
            pan_card_doc = uploaded_files['pan_card_doc']
            domicile_doc = uploaded_files['domicile_doc']
            caste_doc = uploaded_files['caste_doc']
            validity_doc = uploaded_files['validity_doc']
            income_doc = uploaded_files['income_doc']
            ssc_doc = uploaded_files['ssc_doc']
            hsc_doc = uploaded_files['hsc_doc']
            grad_doc = uploaded_files['grad_doc']
            post_grad_doc = uploaded_files['post_grad_doc']
            entrance_doc = uploaded_files['entrance_doc']
            phd_reciept_doc = uploaded_files['phd_reciept_doc']
            guideAllotment_doc = uploaded_files['guideAllotment_doc']
            guideAccept_doc = uploaded_files['guideAccept_doc']
            rac_doc = uploaded_files['rac_doc']
            confirmation_doc = uploaded_files['confirmation_doc']
            joining_doc = uploaded_files['joining_doc']
            annexureAC_doc = uploaded_files['annexureAC_doc']
            annexureB_doc = uploaded_files['annexureB_doc']
            disable_doc = uploaded_files['disable_doc']
            gazete_doc = uploaded_files['gazete_doc']
            selfWritten_doc = uploaded_files['selfWritten_doc']
            research_letter_doc = uploaded_files['research_letter_doc']

            section5 = 'filled'

            if filled_section5 != 'filled':
                print('No Records just insert')
                # Save the form data to the database
                print('Inserting new record for:' + email)
                sql = """
                    UPDATE application_page 
                    SET 
                        signature = %s, adhaar_card_doc = %s, pan_card_doc = %s, domicile_doc = %s, 
                        caste_doc = %s, validity_doc = %s, income_doc = %s, ssc_doc = %s, hsc_doc = %s,
                        grad_doc = %s, post_grad_doc = %s, entrance_doc = %s, phd_reciept_doc = %s, 
                        guideAllotment_doc = %s, guideAccept_doc = %s, rac_doc = %s, confirmation_doc = %s, 
                        joining_doc = %s, annexureAC_doc = %s, annexureB_doc = %s, disable_doc = %s, 
                        gazete_doc = %s, selfWritten_doc = %s, research_letter_doc = %s, section5 = %s
                    WHERE email = %s
                """
                values = (
                    signature, adhaar_card_doc, pan_card_doc, domicile_doc, caste_doc, validity_doc, income_doc,
                    ssc_doc, hsc_doc, grad_doc, post_grad_doc, entrance_doc, phd_reciept_doc, guideAllotment_doc,
                    guideAccept_doc, rac_doc, confirmation_doc, joining_doc, annexureAC_doc, annexureB_doc,
                    disable_doc, gazete_doc, selfWritten_doc, research_letter_doc,
                    section5, email  # Include `email` to identify the record
                )

                cursor.execute(sql, values)
                cnx.commit()

                cursor.execute("SELECT first_name, last_name, email, user, year FROM signup WHERE email = %s",
                               (email,))
                old_user = cursor.fetchone()
                cnx.commit()

                print(old_user)

                year_check = str(old_user['year'])
                print(year_check)
                user_check = old_user['user']

                if year_check in ['2021', '2022'] and user_check == 'Old User':
                    print('Updating Old User Record')
                    # Enter Old User Applicant ID
                    enter_old_applicant_id(email)
                    # Enter Old Presenty Record
                    enter_presenty_record(email)
                else:
                    print('email', email)
                    # Inserts three differnet flags with applicant ID.
                    enter_applicant_id(email)
                    # Checks the email in Presenty and if not inserts it.
                    enter_presenty_record(email)

                # Send Email of Completion
                # send_email_of_completion(email)
                return redirect(url_for('section5.completed_application'))
                # Check if the user is approved for fellowship no matter the year to show the desired sidebar.
            else:
                return redirect(url_for('section5.section5'))
        else:
            # Handle GET request (display empty form, or previously filled data if necessary)
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

            print(current_date)
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

