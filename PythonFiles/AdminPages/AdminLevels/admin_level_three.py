import datetime
from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask_mail import Mail, Message
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, jsonify

adminlevelthree_blueprint = Blueprint('adminlevelthree', __name__)


def adminlevelthree_auth(app, mail):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    def get_admin_level_three_data(year):  # Separate function for data fetching
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        query = """
                   SELECT * FROM application_page 
                   WHERE form_filled='1' 
                   AND fellowship_application_year=%s 
                   AND status='accepted'
                   AND scrutiny_status='accepted'
                """
        cursor.execute(query, (year,))
        data = cursor.fetchall()
        cursor.close()
        cnx.close()
        for row in data:
            for key, value in row.items():
                if isinstance(value, datetime.timedelta):
                    row[key] = str(value)  # Or value.total_seconds()
                elif isinstance(value, datetime.date):
                    row[key] = value.strftime('%Y-%m-%d')
                elif isinstance(value, datetime.datetime):
                    row[key] = value.isoformat()

        return data  # Return the data (list of dictionaries)

    @adminlevelthree_blueprint.route('/get_approval_year_three', methods=['GET', 'POST'])
    def get_approval_year_three():
        year = request.args.get('year', '2024')
        admin_level_three_data = get_admin_level_three_data(year)  # Call the data fetching function
        # print(admin_level_one_data)
        data = {
            'admin_level_three_list': admin_level_three_data
        }
        return jsonify(data)

    @adminlevelthree_blueprint.route('/level_three_admin', methods=['GET', 'POST'])
    def level_three_admin():
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('adminlogin.admin_login'))
        
        user = session['user']
        print("The user is: " + user)
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        try:
            # Fetch admin details
            cursor.execute("SELECT * FROM admin WHERE username = %s", (user,))
            admin_result = cursor.fetchone()

            # Default year selection
            year_selected = "2024"  

            if admin_result:
                admin_year = admin_result['year']
                admin_username = admin_result['username']
                role = admin_result['role']

                # Extract and format username
                first_name = admin_result.get('first_name', '') or ''
                surname = admin_result.get('surname', '') or ''
                username = first_name + ' ' + surname
                if username.strip() in ('None', ''):
                    username = "Admin"

                print("The username is " + username)

                if role == "Admin":
                    if admin_username == "Admin2021" and admin_year == "BANRF 2021":
                        year_selected = "2021"
                    elif admin_username == "Admin2022" and admin_year == "BANRF 2022":
                        year_selected = "2022"
                    elif admin_username == "Admin2023" and admin_year == "BANRF 2023":
                        year_selected = "2023"
                    elif admin_username == "Admin2024" and admin_year == "BANRF.2024":  # Corrected typo here
                        year_selected = "2024"

            # Set available years
            years = ["2020", "2021", "2022", "2023", "2024"]
            # Set available usernames
            usernames = ["Admin2021", "Admin2022", "Admin2023", "Admin2024"]

            print("I am displaying FINAL APPROVAL Report")

            # Get year from request, fallback to admin's assigned year if not provided
            year = request.args.get('year', year_selected)
            print("The year selected is :" +year)

            data = get_admin_level_three_data(year)  # Call the data fetching function

            # print(data)

            # Render template with results
            return render_template(
                'AdminPages/AdminLevels/LevelThree/admin_level_three.html',
                data=data,
                year=year,
                years=years,
                username=username,
                year_selected=year_selected,
                admin_username=admin_username,
                usernames=usernames 
            )

        except Exception as e:
            print(f"Error: {e}")
            flash("An error occurred while fetching data", "error")
            return redirect(url_for('adminlevelthree.level_three_admin'))

        finally:
            # Ensure the cursor and connection are closed properly
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()

    @adminlevelthree_blueprint.route('/accept_at_level_3', methods=['GET', 'POST'])
    def accept_at_level_3():
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('adminlogin.admin_login'))

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        applicant_id = request.form['applicant_id']  # Use the correct field name

        cursor.execute("SELECT * FROM application_page WHERE applicant_id = %s", (applicant_id,))
        user_result = cursor.fetchone()

        final_approval = 'accepted'
        current_date = datetime.date.today()
        current_day_int = int(current_date.strftime("%d"))
        current_month_int = int(current_date.strftime("%m"))
        current_year_int = int(current_date.strftime("%Y"))
        approved_for = '2024'

        update_query = ("UPDATE application_page SET final_approval = %s, final_approved_date = %s, "
                        "final_approval_day = %s, final_approval_month = %s, final_approval_year = %s, "
                        "approved_for = %s  WHERE applicant_id = %s")
        cursor.execute(update_query, (final_approval, current_date, current_day_int, current_month_int,
                                      current_year_int, approved_for, applicant_id))
        cnx.commit()  # Important: Commit the changes to the database

        # To insert 10 records in payment sheet
        insert_payment_sheet_record(applicant_id)

        cursor.execute(
            "SELECT email, first_name, last_name, status, status_rejected_reason, scrutiny_status, "
            "scrutiny_rejected_reason FROM application_page WHERE applicant_id = %s",
            (applicant_id,))  # Include last_name
        user_data = cursor.fetchone()
        print('User Data:', user_data)

        if user_data:
            email = user_data['email']
            first_name = user_data['first_name']
            last_name = user_data['last_name']  # Get last name
            full_name = f"{first_name} {last_name}"  # Correct full name construction

            # send_email_accept(email, full_name, 'Rejected', applicant_id)
        # Commit the changes to the database
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect(url_for('adminlevelthree.level_three_admin'))

    @adminlevelthree_blueprint.route('/reject_at_level_3', methods=['GET', 'POST'])
    def reject_at_level_3():
        """
            This is for Final Approval
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('adminlogin.admin_login'))

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        applicant_id = request.form['applicant_id']  # Use the correct field name
        rejection_reason = request.form['rejectionReason']
        status = 'rejected'
        rejected_at = 'final_approval'
        scrutiny_status = 'rejected'
        final_approval = 'rejected'
        print('User Data:', request.form)

        update_query = ("UPDATE application_page SET status=%s, scrutiny_status=%s, final_approval = %s, final_rejected_reason = %s, "
                        "rejected_at_level = %s, scrutiny_status = %s, final_approval = %s WHERE applicant_id = %s")
        cursor.execute(update_query,
                       (status, status, status, rejection_reason, rejected_at, scrutiny_status, final_approval, applicant_id))
        cnx.commit()  # Important: Commit the changes to the database

        cursor.execute(
            "SELECT email, first_name, last_name, status, status_rejected_reason, scrutiny_status, "
            "scrutiny_rejected_reason FROM application_page WHERE applicant_id = %s",
            (applicant_id,))  # Include last_name
        user_data = cursor.fetchone()
        print('User Data:', user_data)

        if user_data:
            email = user_data['email']
            first_name = user_data['first_name']
            last_name = user_data['last_name']  # Get last name
            full_name = f"{first_name} {last_name}"  # Correct full name construction

            # send_email_rejection(email, full_name, 'Rejected', applicant_id)
        # Commit the changes to the database
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect(url_for('adminlevelthree.level_three_admin'))

    def generate_payment_sheet(applicant_id, email):
        """
            This function is written as whenever the final approval will happen from admin or whoever approves,
            that is the time the payment sheet for 5 years will generate for that student as per the application
            year. Sheets duration will be according to the date of PHD Registration date and will have 10 quarters
            of 6 Months across 5 years of fellowship.
        """
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute(
            "SELECT fellowship_application_year FROM application_page WHERE applicant_id = %s",
            (applicant_id,))
        user_data = cursor.fetchone()
        approved_for = user_data['fellowship_application_year']

        # Update the status and date components for the specified applicant ID
        update_query = "UPDATE application_page SET final_approval = %s, final_approval_day = %s, " \
                       "final_approval_month = %s, final_approval_year = %s, " \
                       "approved_for=%s WHERE applicant_id = %s"
        print(update_query)
        # cursor.execute(update_query, (final_approval, day, month, year, approved_for, applicant_id))

        # Commit the changes to the database
        cnx.commit()

        # Close the cursor and database connection
        cursor.close()
        cnx.close()

    def send_email_approval(email, full_name, status, applicant_id):
        base_url = request.url_root
        # email_body = render_template('email_template.html', full_name=full_name, status=status,  applicant_id=applicant_id)
        # Construct the HTML email body
        msg_body = f'''
           <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        <style>
            @import url('https:                                                                                                                    f  fv  //fonts.googleapis.com/css2?family=Montserrat:wght@100;200;300;400;500;600;700;800;900&display=swap');
        </style>
    </head>

    <body style="background: radial-gradient(rgb(235,236,240),rgb(235,236,240));  margin: 0; font-family: 'Montserrat', sans-serif;  overflow: auto; padding:50px; width:100%;">

        <table style="width: 90%; margin: auto; min-width: 480px; width: 540px;  border-spacing: 0;">
            <tr style="background: #F5F5F5; border-radius: 10px; overflow: hidden;">
                <td style="text-align: center;">
                    <img src="https://fellowship.trti-maha.in/static/assets/img/logo/logo-new.png" style="width: 80px;" alt="TRTI logo">

                </td>
                <td style="text-align: center;">
                    <img src="https://fellowship.trti-maha.in/static/assets/img/fellow_logo_1.png" style="width: 70px;" alt="Fellowship Logo">
                </td>
                <td style="text-align: center;">
                    <h3 style="color: #175E97; font-weight: 700; ">FELLOWSHIP</h3>
                </td>
                <td style="text-align: center;">
                    <h3 style="color: #B71540; font-weight: 600; font-size: 15px;">HOME</h3>
                </td>
                <td style="text-align: center;">
                    <h3 style="color: #B71540; font-weight: 600; font-size: 15px;">CONTACT US</h3>
                </td>
            </tr>
            <tr>
                <td colspan="5"
                    style="background: linear-gradient(rgba(169,27,96,0.4), rgba(169,27,96,0.4)), url('https://fellowship.trti-maha.in/static/assets/img/banner_award.jpg'); width: 100%; height: 30vh; background-size: cover; background-repeat: no-repeat;">
                    <h2 style="text-transform: uppercase; text-align: center; font-size: 50px; color: #fff;">Congratulations
                    </h2>
                </td>
            </tr>
            <tr>
                <td colspan="5" style="background: #fff; padding: 40px;">
                    <h4
                        style="text-transform: uppercase; text-align: center; font-size: 20px; font-weight: 600; color: #A91B60;">
                        Hello, {full_name}</h4>
                    <h4
                        style="text-transform: uppercase; text-align: center; font-size: 18px; font-weight: 600; color: #A91B60; line-height: 28px;">
                        Congratulations The Status Of Your Application Has Changed To Accepted!! Please Login To View The
                        Status As Accepted For Fellowship</h4>
                    <h4
                        style="text-transform: uppercase; text-align: center; font-size: 18px; font-weight: 600; color: #A91B60; line-height: 28px;">
                        Your Application ID:</h4>
                    <p
                        style="text-align: center; padding: 25px; border: 3px solid #ECB322; color: #ECB322; font-weight: 700; letter-spacing: 10px; font-size: 20px;">
                        {applicant_id}</p>
                </td>
            </tr>
            <tr>
                <td colspan="5" style="background: #A91B60; padding: 40px;">
                    <h4
                        style="text-transform: uppercase; text-align: center; font-size: 18px; font-weight: 600; color: #fff; line-height: 28px;">
                        Please Upload Your Joing Report as soon as you get it signed by concerned authority</h4>
                </td>
            </tr>
            <tr>
                <td colspan="5" style="background: #fff; padding: 40px;">
                    <h4
                        style="text-transform: uppercase; text-align: center; font-size: 12px; font-weight: 600; color: #A91B60; line-height: 18px;">In case of any technical issue while filling online application form, please contact on toll free helpline number No. (From 09:45 AM to 06:30) PM </h4>
                    <p style="color:#A91B60; font-size: 11px; font-weight: 600; text-align: center;">
                        This is a system generated mail. Please do not reply to this Email ID
                    </p>
                </td>
            </tr>
            <tr>
                <td colspan="5" style="background: #A91B60; padding: 10px 40px; ">
                   <span style="color: #fff; font-size: 11px; ">Visit us at <a href="https://trti.maharashtra.gov.in" target="_blank" style="color: #fff;">https://trti.maharashtra.gov.in</a> </span>
                    <img src="https://static.vecteezy.com/system/resources/thumbnails/027/395/710/small/twitter-brand-new-logo-3-d-with-new-x-shaped-graphic-of-the-world-s-most-popular-social-media-free-png.png" style="width: 32px; height: 32px; float: right; " alt="Twitter Logo">
                    <img src="https://cdn3.iconfinder.com/data/icons/social-network-30/512/social-06-512.png" style="width: 32px;  height: 32px;  float: right; margin-right: 12px; background: transparent;" alt="Youtube Logo">
                   <img src="https://freelogopng.com/images/all_img/1658030214facebook-logo-hd.png" style="width: 32px; height: 32px; float: right; margin-right: 12px; " alt="Facebok Logo">
                </td>
            </tr>
        </table>

    </body>

    </html>

        '''

        # Email content in HTML format
        msg = Message('Application Status Changed', sender='noreply_fellowship@trti-maha.in', recipients=[email])
        msg.html = msg_body
        mail.send(msg)

    def send_email_rejection(email, full_name, status, applicant_id):
        # Email content in HTML format
        msg = Message('Application Status Changed', sender='helpdesk@trti-maha.in', recipients=[email])
        # msg.body = msg.body = "Hi, " + full_name + "\n Your Status for Fellowship : " + status + \
        #                       "\n Unfortunately the status of your application has changed to Rejected!!" + \
        #                       "\n Please login to view the status as Accepted for Fellowship" + \
        #                       "\n Your Application ID = " + applicant_id

        msg_body = f''' 
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@100;200;300;400;500;600;700;800;900&display=swap');


        </style>
    </head>

    <body style="background: radial-gradient(rgb(235,236,240),rgb(235,236,240)); padding: 50px;  margin: 0;  font-family: 'Montserrat', sans-serif;">

        <table style="width: 90%; margin: auto; min-width: 480px; border-radius: 10px; overflow: hidden; width: 540px; border-spacing: 0;">
            <tr style="background: #F5F5F5; border-radius: 10px; ">
                <td style="text-align: center;">
                    <img src="https://fellowship.trti-maha.in/static/assets/img/logo/logo-new.png" style="width: 80px;"
                        alt="TRTI logo">

                </td>
                <td style="text-align: center;">
                    <img src="https://fellowship.trti-maha.in/static/assets/img/fellow_logo_1.png" style="width: 70px;"
                        alt="Fellowship Logo">
                </td>
                <td style="text-align: center;">
                    <h3 style="color: #175E97; font-weight: 700; ">FELLOWSHIP</h3>
                </td>
                <td style="text-align: center;">
                    <h3 style="color: #B71540; font-weight: 600; font-size: 15px;">HOME</h3>
                </td>
                <td style="text-align: center;">
                    <h3 style="color: #B71540; font-weight: 600; font-size: 15px;">CONTACT US</h3>
                </td>
            </tr>
            <tr>
                <td colspan="5"
                    style="background: linear-gradient(rgba(169,27,96,0.4), rgba(169,27,96,0.4)), url('https://fellowship.trti-maha.in/static/assets/img/banner_award.jpg'); width: 100%; height: 30vh; background-size: cover; background-repeat: no-repeat;">
                    <h2
                        style="text-transform: uppercase; text-align: center; font-size: 50px; color: #fff; width: 90%; letter-spacing: 5px; margin: auto; ">
                        Thanks For Applying
                    </h2>
                </td>
            </tr>
            <tr>
                <td colspan="5" style="background: #fff; padding: 40px;">
                    <h4
                        style="text-transform: uppercase; text-align: center; font-size: 20px; font-weight: 600; color: #A91B60;">
                        Hello, {full_name}</h4>
                    <h4
                        style="text-transform: uppercase; text-align: center; font-size: 18px; font-weight: 600; color: #A91B60; line-height: 28px;">
                        Your Status for Fellowship : {status}
                        Unfortunately the status of your application has changed to Rejected!!
                    </h4>
                    <h4
                        style="text-transform: uppercase; text-align: center; font-size: 18px; font-weight: 600; color: #A91B60; line-height: 28px;">
                        Please Login To View The Status As Rejected For Fellowship
                    </h4>
                    <h4
                        style="text-transform: uppercase; text-align: center; font-size: 18px; font-weight: 600; color: #A91B60; line-height: 28px;">
                        Your Application ID:</h4>
                    <p
                        style="text-align: center; padding: 25px; border: 3px solid #ECB322; color: #ECB322; font-weight: 700; letter-spacing: 10px; font-size: 20px;">{applicant_id}</p>
                </td>
            </tr>
            <tr>
                <td colspan="5" style="background: #fff; padding: 40px; border-top: 1px solid rgb(235,236,240);">
                    <h4
                        style="text-transform: uppercase; text-align: center; font-size: 12px; font-weight: 600; color: #A91B60; line-height: 18px;">
                        In case of any technical issue while filling online application form, please contact on toll free
                        helpline number 18002330444 (From 09:45 AM to 06:30 PM </h4>
                    <p style="color:#A91B60; font-size: 11px; font-weight: 600; text-align: center;">
                        This is a system generated mail. Please do not reply to this Email ID
                    </p>
                </td>
            </tr>
            <tr>
                <td colspan="5" style="background: #A91B60; padding: 10px 40px; ">
                    <span style="color: #fff; font-size: 11px; ">Visit us at <a href="https://trti.maharashtra.gov.in"
                            target="_blank" style="color: #fff;">https://trti.maharashtra.gov.in</a> </span>
                    <img src="https://static.vecteezy.com/system/resources/thumbnails/027/395/710/small/twitter-brand-new-logo-3-d-with-new-x-shaped-graphic-of-the-world-s-most-popular-social-media-free-png.png" style="width: 32px; height: 32px; float: right; " alt="Twitter Logo">
                    <img src="https://cdn3.iconfinder.com/data/icons/social-network-30/512/social-06-512.png"
                        style="width: 32px;  height: 32px;  float: right; margin-right: 12px; background: transparent;"
                        alt="Youtube Logo">
                    <img src="https://freelogopng.com/images/all_img/1658030214facebook-logo-hd.png"
                        style="width: 32px; height: 32px; float: right; margin-right: 12px; " alt="Facebok Logo">
                </td>
            </tr>
        </table>

    </body>

    </html> 
    '''
        msg = Message('Application Status Changed', sender='noreply_fellowship@trti-maha.in', recipients=[email])
        msg.html = msg_body
        mail.send(msg)

    # @adminlevelthree_blueprint.route('/accepted_students_level3', methods=['GET', 'POST'])
    # def accepted_students_level3():
    #     host = HostConfig.host
    #     connect_param = ConnectParam(host)
    #     cnx, cursor = connect_param.connect(use_dict=True)
    #     cursor.execute(" SELECT * FROM application_page WHERE fellowship_application_year='2024' and "
    #                    "final_approval='accepted' and scrutiny_status='accepted' ")
    #     result = cursor.fetchall()
    #
    #     return render_template('AdminPages/AdminLevels/LevelThree/accepted_students_level3.html', result=result)
    #
    # @adminlevelthree_blueprint.route('/pending_students_level3', methods=['GET', 'POST'])
    # def pending_students_level3():
    #     host = HostConfig.host
    #     connect_param = ConnectParam(host)
    #     cnx, cursor = connect_param.connect(use_dict=True)
    #     cursor.execute(" SELECT * FROM application_page WHERE fellowship_application_year='2024' "
    #                    "and final_approval='pending' and scrutiny_status='accepted' ")
    #     result = cursor.fetchall()
    #     print('Pending', result)
    #     return render_template('AdminPages/AdminLevels/LevelThree/pending_students_level3.html', result=result)
    #
    # @adminlevelthree_blueprint.route('/rejected_students_level3')
    # def rejected_students_level3():
    #     host = HostConfig.host
    #     connect_param = ConnectParam(host)
    #     cnx, cursor = connect_param.connect(use_dict=True)
    #     cursor.execute(" SELECT * FROM application_page WHERE fellowship_application_year='2024' "
    #                    "and final_approval='rejected' and scrutiny_status='accepted' ")
    #     result = cursor.fetchall()
    #
    #     return render_template('AdminPages/AdminLevels/LevelThree/rejected_students_level3.html', result=result)
    #
    # @adminlevelthree_blueprint.route('/pvtg_students_level3')
    # def pvtg_students_level3():
    #     host = HostConfig.host
    #     connect_param = ConnectParam(host)
    #     cnx, cursor = connect_param.connect(use_dict=True)
    #     cursor.execute(
    #         " SELECT * FROM application_page WHERE fellowship_application_year='2024' and"
    #         " your_caste IN ('katkari', 'kolam', 'madia') "
    #     )
    #     result = cursor.fetchall()
    #     return render_template('AdminPages/AdminLevels/LevelThree/pvtg_students_level3.html', result=result)
    #
    # @adminlevelthree_blueprint.route('/disabled_students_level3')
    # def disabled_students_level3():
    #     host = HostConfig.host
    #     connect_param = ConnectParam(host)
    #     cnx, cursor = connect_param.connect(use_dict=True)
    #     cursor.execute(
    #         " SELECT * FROM application_page WHERE fellowship_application_year='2024' and disability='Yes' "
    #     )
    #     result = cursor.fetchall()
    #     return render_template('AdminPages/AdminLevels/LevelThree/disabled_students_level3.html', result=result)


    # def insert_payment_sheet_record():
    def insert_payment_sheet_record(applicant_id):
        """
        This function is also written in Section5.py for Old Users as they are already accepted.
        Here it is for new users.
        """
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        payment_records = []

        cursor.execute("SELECT * FROM application_page WHERE applicant_id = %s", (applicant_id,))
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
            fellowship_awarded_year = result['fellowship_awarded_year']
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
            return flash('Record Inserted Successfully', 'success')
        else:
            error = flash('No record Found', 'error')
            return error




