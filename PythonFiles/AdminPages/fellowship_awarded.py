from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, Response
from PythonFiles.AdminPages.PDFfile import *
import datetime

fellowship_awarded_blueprint = Blueprint('fellowship_awarded', __name__)


def fellowship_awarded_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @fellowship_awarded_blueprint.route('/fellowship_awarded', methods=['GET', 'POST'])
    def fellowship_awarded():
        if not session.get('logged_in'):
            return redirect(url_for('adminlogin.admin_login'))

        user = session['user']
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute("SELECT * FROM admin WHERE username = %s", (user,))
        admin_result = cursor.fetchone()
        admin_year = admin_result['year']
        admin_username = admin_result['username']
        role = admin_result['role']

        year_selected = None

        if role == "Admin" and admin_username == "Admin2021" and admin_year == "BANRF 2021":
            year_selected = "2021"
        elif role == "Admin" and admin_username == "Admin2022" and admin_year == "BANRF 2022":
            year_selected = "2022"
        elif role == "Admin" and admin_username == "Admin2023" and admin_year == "BANRF 2023":
            year_selected = "2023"
        elif role == "Admin" and admin_username == "Admin2024" and admin_year == "BANRF.2024":
            year_selected = "2024"

        sql = """
            SELECT *
            FROM application_page
            WHERE final_approval = 'accepted'
        """

        if year_selected:
            sql += " AND approved_for = %s"
            cursor.execute(sql, (year_selected,))
        else:
            sql += " AND approved_for IN ('2020', '2021', '2022', '2023', '2024')"
            cursor.execute(sql)

        result = cursor.fetchall()
        cursor.close()
        cnx.close()
        return render_template('AdminPages/fellowship_awarded.html', result=result)

    @fellowship_awarded_blueprint.route('/generate_pdf_application/<string:email>', methods=['GET', 'POST'])
    def generate_pdf_application(email):
        # email = session['email']
        output_filename = app.config['PDF_STORAGE_PATH']
        # output_filename = '/static/pdf_application_form/pdfform.pdf'

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute(" SELECT * FROM signup WHERE year IN ('2020', '2021', '2022') and email = %s ", (email,))
        output = cursor.fetchall()

        if output:
            cursor.execute(
                "SELECT * FROM application_page WHERE email = %s", (email,))
            old_user_data = cursor.fetchone()
            print(old_user_data)
            # Generate a styled PDF
            print(output_filename)
            generate_pdf_with_styling(old_user_data, output_filename)
        else:
            cursor.execute("SELECT * FROM application_page WHERE email = %s", (email,))
            data = cursor.fetchone()
            print(data)
            # Generate a styled PDF
            generate_pdf_with_styling(data, output_filename)

        # Serve the generated PDF as a response
        with open(output_filename, "rb") as pdf_file:
            response = Response(pdf_file.read(), content_type="application/pdf")
            response.headers['Content-Disposition'] = 'inline; filename=pdfform.pdf'

        return response

    @fellowship_awarded_blueprint.route('/generate_award_letter_AA/<string:email>')
    def generate_award_letter_AA(email):
        try:
            # email = session['email']
            output_filename = '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/pdf_application_form/award_letter.pdf'
            # output_filename = 'static/pdf_application_form/pdfform.pdf'

            host = HostConfig.host
            connect_param = ConnectParam(host)
            cnx, cursor = connect_param.connect(use_dict=True)

            cursor.execute(
                "SELECT id, applicant_photo, applicant_id, adhaar_number, first_name, last_name, middle_name, mobile_number,"
                " email, date_of_birth, gender, age, caste, your_caste, marital_status, dependents, state, district,"
                " taluka, village, city, add_1, add_2, pincode, ssc_passing_year,"
                " ssc_percentage, ssc_school_name, hsc_passing_year, hsc_percentage, hsc_school_name,"
                " graduation_passing_year, graduation_percentage, graduation_school_name, phd_passing_year,"
                " phd_percentage, phd_school_name,have_you_qualified, name_of_college, name_of_guide, topic_of_phd,"
                " concerned_university, faculty, phd_registration_date, phd_registration_year,"
                " family_annual_income, "
                " income_certificate_number, issuing_authority, domicile, domicile_certificate, domicile_number,"
                " caste_certf, issuing_district, caste_issuing_authority, salaried, disability, type_of_disability,"
                " father_name, mother_name, work_in_government, bank_name, account_number, ifsc_code,"
                " account_holder_name, application_date FROM application_page WHERE email = %s", (email,))
            data = cursor.fetchone()

            cursor.execute(
                "SELECT id, phd_registration_year FROM application_page WHERE email = %s",
                (email,))
            result = cursor.fetchone()
            year = result['phd_registration_year']
            id = result['id']

            # Below function is defined in AdminPages/PDFfile.py - Displays the Award letter
            generate_award_letter(data, output_filename)

            # Serve the generated PDF as a response
            with open(output_filename, "rb") as pdf_file:
                response = Response(pdf_file.read(), content_type="application/pdf")
                response.headers['Content-Disposition'] = 'inline; filename=award_letter.pdf'
        except BrokenPipeError:
            # Handle broken pipe error, e.g., log it
            pass

        return response

    @fellowship_awarded_blueprint.route('/award_fellowships/<int:id>', methods=['GET', 'POST'])
    def award_fellowships(id):
        # applicant_id = request.view_args['applicant_id']
        # print(applicant_id)
        # Initialize database connection
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        try:
            # Fetch the record based on ID
            sql = """SELECT * FROM application_page WHERE id = %s"""
            cursor.execute(sql, (id,))
            records = cursor.fetchone()

            # print('Recor?ds', records)

            # Handle case where no record is found
            if not records:
                flash("Record not found.", "error")
                return redirect(url_for('fellowship_awarded.fellowship_awarded'))

            # Extract email from the fetched record
            email = records['email']

            if request.method == 'POST':
                # Handle POST request
                accepted_list = request.form['accepted_list']

                fellowship_awarded_date = request.form['fellowship_awarded_date']
                fellowship_awarded_year = request.form['fellowship_awarded_year']
                year = request.form['year']
                case_number = request.form['case_number']
                desk_number = request.form['desk_number']
                unique_id = request.form['unique_id']

                outward_number = f"Research-{year}/Case.No {case_number}/Desk-{desk_number}/{unique_id}"

                # Get current date and time
                # n?ow = datetime.datetime.now()
                current_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Fixed format for date
                current_time = datetime.datetime.now().strftime('%H:%M:%S')  # Fixed format for time

                # Update the record
                update_query = """
                    UPDATE application_page 
                    SET accepted_list=%s, fellowship_awarded_date=%s,
                        fellowship_awarded_year=%s, outward_number=%s, joining_date=%s, fellowship_awarded=%s,
                        awardletter_awarded_date=%s, awardletter_awarded_time=%s
                    WHERE email = %s
                """
                cursor.execute(update_query,
                               (accepted_list, fellowship_awarded_date, fellowship_awarded_year, outward_number,
                                fellowship_awarded_date, 'Awarded', current_date, current_time, email))
                cnx.commit()

                # Set session and redirect
                # session['change_center'] = True
                flash("Award Letter has been awarded to the student successfully.", "success")
                return redirect(url_for('fellowship_awarded.fellowship_awarded'))

            else:
                # Redirect for non-POST requests
                return redirect(url_for('fellowship_awarded.fellowship_awarded'))

        except Exception as e:
            # Log the exception (optional)
            print(f"Error: {e}")
            flash("An error occurred. Please try again.", "error")
            return redirect(url_for('fellowship_awarded.fellowship_awarded'))

        finally:
            # Ensure connection is closed
            cursor.close()
            cnx.close()

