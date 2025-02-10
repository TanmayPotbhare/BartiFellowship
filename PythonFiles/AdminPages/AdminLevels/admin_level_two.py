import datetime
import mysql.connector
from classes.database import HostConfig, ConfigPaths, ConnectParam
import os
from flask_mail import Mail, Message
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, jsonify
from Authentication.middleware import auth

adminleveltwo_blueprint = Blueprint('adminleveltwo', __name__)


def adminleveltwo_auth(app, mail):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    def get_admin_level_two_data(year):  # Separate function for data fetching
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        query = """
                   SELECT * FROM application_page 
                   WHERE form_filled='1' 
                   AND fellowship_application_year=%s 
                   AND status='accepted'
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

    @adminleveltwo_blueprint.route('/get_approval_year_two', methods=['GET', 'POST'])
    def get_approval_year_two():
        year = request.args.get('year', '2024')
        admin_level_two_data = get_admin_level_two_data(year)  # Call the data fetching function
        # print(admin_level_one_data)
        data = {
            'admin_level_two_list': admin_level_two_data
        }
        return jsonify(data)

    @adminleveltwo_blueprint.route('/level_two_admin', methods=['GET', 'POST'])
    def level_two_admin():
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('adminlogin.admin_login'))
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        year = request.args.get('year', '2024')  # Get the year from the URL parameter (for initial load)
        data = get_admin_level_two_data(year)

        return render_template('AdminPages/AdminLevels/LevelTwo/admin_level_two.html', data=data)

    @adminleveltwo_blueprint.route('/accept_at_level_2', methods=['GET', 'POST'])
    def accept_at_level_2():
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('adminlogin.admin_login'))

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        applicant_id = request.form['applicant_id']  # Use the correct field name
        status = 'accepted'
        print('User Data:', request.form)

        update_query = "UPDATE application_page SET scrutiny_status = %s WHERE applicant_id = %s"  # Correct SQL syntax
        cursor.execute(update_query, (status, applicant_id))
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

            # send_email_accept(email, full_name, 'Rejected', applicant_id)
        # Commit the changes to the database
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect(url_for('adminleveltwo.level_two_admin'))

    @adminleveltwo_blueprint.route('/reject_at_level_2', methods=['GET', 'POST'])
    def reject_at_level_2():
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('adminlogin.admin_login'))

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        applicant_id = request.form['applicant_id']  # Use the correct field name
        rejection_reason = request.form['rejectionReason']
        status = 'rejected'
        rejected_at = 'scrutiny'
        scrutiny_status = 'rejected'
        final_approval = 'rejected'
        print('User Data:', request.form)

        update_query = ("UPDATE application_page SET status = %s, scrutiny_rejected_reason = %s, "
                        "rejected_at_level = %s, scrutiny_status = %s, final_approval = %s WHERE applicant_id = %s")
        cursor.execute(update_query,
                       (status, rejection_reason, rejected_at, scrutiny_status, final_approval, applicant_id))
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
        return redirect(url_for('adminleveltwo.level_two_admin'))

    def update_scrutiny_admin(applicant_id, scrutiny_status):
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        # Update the status for the specified applicant ID
        update_query = "UPDATE application_page SET scrutiny_status = %s WHERE applicant_id = %s"
        cursor.execute(update_query, (scrutiny_status, applicant_id))

        # Commit the changes to the database
        cnx.commit()

        # Close the cursor and database connection
        cursor.close()
        cnx.close()

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

    @adminleveltwo_blueprint.route('/accepted_students_level2', methods=['GET', 'POST'])
    def accepted_students_level2():
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('adminlogin.admin_login'))
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute(" SELECT * FROM application_page WHERE fellowship_application_year='2024' and "
                       "scrutiny_status='accepted' and status='accepted' ")
        result = cursor.fetchall()

        return render_template('AdminPages/AdminLevels/LevelTwo/accepted_students_level2.html', result=result)

    @adminleveltwo_blueprint.route('/pending_students_level2', methods=['GET', 'POST'])
    def pending_students_level2():
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)
        cursor.execute(
            " SELECT * FROM application_page WHERE fellowship_application_year='2024' and scrutiny_status='pending' "
            "and status='accepted' ")
        result = cursor.fetchall()
        print('Pending', result)
        return render_template('AdminPages/AdminLevels/LevelTwo/pending_students_level2.html', result=result)

    @adminleveltwo_blueprint.route('/rejected_students_level2')
    def rejected_students_level2():
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)
        cursor.execute(" SELECT * FROM application_page WHERE fellowship_application_year='2024' "
                       "and scrutiny_status='rejected' and status='accepted' ")
        result = cursor.fetchall()

        return render_template('AdminPages/AdminLevels/LevelTwo/rejected_students_level2.html', result=result)

    @adminleveltwo_blueprint.route('/pvtg_students_level2')
    def pvtg_students_level2():
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)
        cursor.execute(
            " SELECT * FROM application_page WHERE fellowship_application_year='2024' and"
            " your_caste IN ('katkari', 'kolam', 'madia') "
        )
        result = cursor.fetchall()
        return render_template('AdminPages/AdminLevels/LevelTwo/pvtg_students_level2.html', result=result)

    @adminleveltwo_blueprint.route('/disabled_students_level2')
    def disabled_students_level2():
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)
        cursor.execute(
            " SELECT * FROM application_page WHERE fellowship_application_year='2024' and disability='Yes' "
        )
        result = cursor.fetchall()
        return render_template('AdminPages/AdminLevels/LevelTwo/disabled_students_level2.html', result=result)