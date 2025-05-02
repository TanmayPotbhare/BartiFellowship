import random
import bcrypt
import mysql.connector
import os
import requests
import re
from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash

# MULTILINGUAL CONTENT - FROM HOMEPAGE_FILES FOLDER
from PythonFiles.Homepage.multilingual_content import multilingual_content

# load_dotenv()

login_blueprint = Blueprint('login_signup', __name__)


def login_auth(app, mail):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    app.config['ZEPTOMAIL_URL'] = "https://api.zeptomail.in/v1.1/email"
    app.config['ZEPTOMAIL_API_KEY'] = "Zoho-enczapikey PHtE6r0PFOjriWB+oRJR5f+wR5L2No0n9O1nfwZG4tkWDKJXGk1d/tosxjO+rhZ/BvlGQPPKmd5gsOvJuuqDJm68NGgdXWqyqK3sx/VYSPOZsbq6x00asF4YdkTVVoPpdtNi0iDfuNuX"


    # ---------------------------------
    #           LOGIN ROUTE
    # ---------------------------------
    @login_blueprint.route('/login', methods=['GET', 'POST'])
    def login():
        """
            This function is used for logging in.
            It has language code which changes to marathi and English, followed by,
            Establishing the connection to database to live server, followed by,
            If the request method is POST then it checks for the username and password entered are right, or if empty
            and give the apt response in the form of sweet alert, followed by,
            checking the password is encrypted or not if yes then routing to the defined route and if the password is
            plain text then routing to the defined routes.
            :param: Email, ID, Session
            :return: Returns all kinds of arrays and dictionaries according to the database queries.
        """
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'

        try:
            host = HostConfig.host
            connect_param = ConnectParam(host)
            cnx, cursor = connect_param.connect(use_dict=True)

            if request.method == 'POST':
                email = request.form['email']
                password = request.form['password']
                print(email)
                # print(password)

                # Validate that both email and password are provided
                if not email or not password:
                    flash('Please enter username and password.', 'error')
                    return redirect(url_for('login_signup.login'))

                # Validate the email format
                email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_regex, email):
                    flash('Please enter a valid email address.', 'error')
                    return redirect(url_for('login_signup.login'))

                # Check if email and password are valid from signup table
                sql = "SELECT email, password, first_name, last_name, year FROM signup WHERE email=%s"
                cursor.execute(sql, (email,))
                user = cursor.fetchone()

                sql = "SELECT formfilled_again FROM application_page WHERE email=%s"
                cursor.execute(sql, (email,))
                user_result = cursor.fetchone()

                if user:
                    user_password = user['password']
                    special_email = ['sveenashri@gmail.com']

                    # If the password is not hashed
                    if not user_password.startswith("$2b$"):
                        if password == user_password:
                            session['email'] = email
                            sql = "SELECT applicant_photo FROM application_page WHERE email=%s"
                            cursor.execute(sql, (email,))
                            user_image = cursor.fetchone()
                            session['applicant_photo'] = user_image[
                                'applicant_photo'] if user_image else '/static/assets/img/default_user.png'

                            if is_withdrawn(email):
                                flash('You have withdrawn from Fellowship. Please BARTI office for any queries.', 'info')
                                return redirect(url_for('login_signup.login'))
                            elif unlocked_application_form(email):
                                session['logged_in_from_login'] = True
                                print('I am unlocked Application Form') 
                                return redirect(url_for('section1.section1'))
                            elif check_final_approval(email):
                                print('I am here 2')
                                session['final_approval'] = "accepted"
                                session['logged_in_from_login'] = True
                                session['show_login_flash'] = True
                                return redirect(url_for('candidate_dashboard.candidate_dashboard'))
                            elif old_user(email):
                                print('I am here')
                                session['logged_in_from_login'] = True
                                session['old_user'] = True
                                return redirect(url_for('section1.old_change_password'))
                            elif new_applicant_incomplete_form(email) == '2024':
                                print('I am here 1')
                                session['logged_in_from_login'] = True
                                return redirect(url_for('section1.app_form_info'))
                            elif is_form_filled(email):
                                print('I am here 3')
                                session['final_approval'] = "pending"
                                id = get_id_by_email(email)
                                session['logged_in_from_login'] = True
                                session['show_login_flash'] = True
                                return redirect(url_for('candidate_dashboard.candidate_dashboard', id=id))
                            else:
                                flash('Redirecting to login closed page for 2023.', 'info')
                                return redirect(url_for('section1.section1'))
                                # return redirect(url_for('login_closed_2023'))
                        else:
                            flash('Invalid password. Please try again.', 'error')
                            return redirect(url_for('login_signup.login'))

                    # For bcrypt hashed passwords
                    elif bcrypt.checkpw(password.encode('utf-8'), user_password.encode('utf-8')):
                        session['email'] = email
                        sql = "SELECT applicant_photo FROM application_page WHERE email=%s"
                        cursor.execute(sql, (email,))
                        user_image = cursor.fetchone()
                        session['applicant_photo'] = user_image[
                            'applicant_photo'] if user_image else '/static/assets/img/default_user.png'

                        if is_withdrawn(email):
                            flash('You have withdrawn from Fellowship. Please BARTI office for any queries.', 'info')
                            return redirect(url_for('login_signup.login'))
                        elif unlocked_application_form(email):
                            session['logged_in_from_login'] = True
                            print('I am unlocked Application Form') 
                            return redirect(url_for('section1.section1'))
                        elif check_final_approval(email):
                            print('I am here 2')
                            session['final_approval'] = "accepted"
                            session['logged_in_from_login'] = True
                            session['show_login_flash'] = True
                            return redirect(url_for('candidate_dashboard.candidate_dashboard'))
                        elif old_user(email):
                            flash('Logged in Succesfully.', 'success')
                            session['logged_in_from_login'] = True
                            return redirect(url_for('section1.app_form_info'))
                        elif new_applicant_incomplete_form(email) == '2024':
                            print('I am here 1')
                            session['logged_in_from_login'] = True
                            return redirect(url_for('section1.app_form_info'))
                        elif is_form_filled(email):
                            print('I am here 3')
                            session['final_approval'] = "pending"
                            id = get_id_by_email(email)
                            session['logged_in_from_login'] = True
                            session['show_login_flash'] = True
                            return redirect(url_for('candidate_dashboard.candidate_dashboard', id=id))
                        else:
                            print('I am here 4')
                            flash('Logged in Succesfully.', 'success')
                            session['logged_in_from_login'] = True
                            return redirect(url_for('section1.app_form_info'))
                            # return redirect(url_for('login_closed_2023'))
                    else:
                        flash('Invalid password. Please try again.', 'error')
                        return redirect(url_for('login_signup.login'))
                else:
                    flash('Invalid Email or Password. Please enter valid credentials.', 'error')
                    return redirect(url_for('login_signup.login'))

        except mysql.connector.Error as err:
            flash(f'Database error: {err}', 'error')
            return redirect(url_for('login_signup.login'))
        except Exception as e:
            flash(f'An error occurred: {e}', 'error')
            return redirect(url_for('login_signup.login'))

        return render_template('Homepage/login.html', language=language, multilingual_content=multilingual_content)

    # ---------------------- Withdraw Applications ----------------------------
    def is_withdrawn(email):
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect()
        sql = """ SELECT fellowship_withdrawn='withdrawn' FROM signup WHERE email=%s"""
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        return result[0]

    # ---------------------- Check for Old Users ----------------------------
    def old_user(email):
        """
            This function checks for the user if he is an old user.
            Which means if the user is registered before the year 2023.
            :param email: Email is attempting to log in.
            :return: Returns the email if it is in the year 2021, 2022, 2020
        """
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect()
        # Corrected SQL query
        sql = """

                SELECT *
                FROM signup
                WHERE email = %s
                  AND year IN ('2020', '2021', '2022', '2023') 
                  AND user = 'Old User'

        """
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        if result:
            print(result)
        cursor.close()
        cnx.close()
        return result if result else None

    # ------------- Check New Applicants Incomplete Form ---------------------
    def new_applicant_incomplete_form(email):  # -------------- CHECK IF USER HAS FILLED THE FORM
        """
            Checks for the condition while a user is logging in.
            Checks if the user is new user by checking the form_filled column in Database.
            :param email: Email is attempting to Log in.
            :return: Returns the form is filled or not by giving 0 and 1 values for New user.
        """
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)
        sql = """
                SELECT year
                FROM signup
                WHERE email = %s;
        """
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        # print(result)
        cursor.close()
        cnx.close()
        return result['year'] is not None

    # -------------------- Check for Finally Approved Students ---------------
    def check_final_approval(email):  # ----------- CHECK IF USER IS FINALLY APPROVED
        """
            This function checks whether the user is accepted for fellowship.
            :param email: Email is attempting to log in.
            :return: Returns the final_approval column from database for the entered email id.
        """
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect()
        sql = "SELECT final_approval FROM application_page WHERE email = %s AND final_approval = 'accepted'"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        if result:
            flash('Please enter correct Email address', 'error')
        else:
            flash('Successfully Logged in', 'success')
        return result is not None

    # ------------------ Check if the form is filled -------------------------
    def is_form_filled(email):  # -------------- CHECK IF USER HAS FILLED THE FORM
        """
            Checks for all the applicants in the database whether the form is filled or not.
            :param email: Email is attempting to log in.
            :return: Returns the form_filled dictionary from the database where value is 1 (1 means form is filled).
        """
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect()
        sql = "SELECT form_filled FROM application_page WHERE form_filled='1' and email=%s"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        return result is not None

    # ----------------- Get ID by Email -------------------------------
    def get_id_by_email(email):  # --------------- GET ID for EMAIL IN SESSION
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect()
        sql = """ SELECT id FROM application_page WHERE email=%s"""
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        print(result[0])
        cursor.close()
        cnx.close()
        return result[0]


    def unlocked_application_form(email):  # ----------- CHECK IF THE FORM IS UNLOCKED
        """
            This function checks whether the application form is unlocked
            :param email: Email is attempting to log in.
            :return: Returns the lock_application_form column from database for the entered email id.
            These forms are unlocked from backend. Hance form_filled = '1' AND lock_application_form = 'unlocked'.
        """
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect()
        sql = "SELECT lock_application_form FROM application_page WHERE email = %s AND lock_application_form = 'unlocked' AND form_filled = '1' "
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        print(result)
        cursor.close()
        cnx.close()
        if result:
            flash('Successfully Logged in. Your application is unlocked. You may now review and modify your information.', 'success')
        else:
           flash('Please enter correct Email address', 'error')
        return result is not None    
    # ---------------------------------
    #           END LOGIN ROUTE
    # ---------------------------------

    # ---------------------------------
    #           LOGOUT ROUTE
    # ---------------------------------
    @login_blueprint.route('/logout')
    def logout():
        """
            This function logs out of the session and redirects to login page.
        :return: Returns to Login Page.
        """
        # Check if the user is logged in before logging out
        if 'email' in session:
            # Clear the session variables related to the user
            session.pop('email', None)
            session.pop('user_name', None)
            session.pop('final_approval', None)
            session.pop('logged_in_from_login', None)
            session.clear()
            return redirect(url_for('login_signup.login'))  # Redirect to the login page after logout
        else:
            return redirect(url_for('adminlogin.admin_login'))
    # ---------------------------------
    #          END LOGOUT ROUTE
    # ---------------------------------

    # ---------------------------------
    #          SIGN UP ROUTE
    # ---------------------------------
    @login_blueprint.route('/signup', methods=['GET', 'POST'])
    def signup():  # --------------------------  SIGN UP PAGE
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'

        if request.method == 'POST':
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            last_name = request.form['last_name']
            email = request.form['email']
            password = request.form['signup_password']
            confirm_password = request.form['confirm_password']
            year = request.form['year']
            mobile_number = request.form['mobile_number']

            if not email or not password:
                flash('Please enter email and password.', 'error')
                return redirect(url_for('login_signup.login'))

            # Check if the passwords match
            if password != confirm_password:
                flash('Please enter the Password Correctly as it does not match', 'error')
                return redirect(url_for('login_signup.login'))

            if old_user(email):
                flash('Please Login with the registered email ID and Password for your login will be Fellowship123. Please change the password after login.', 'error')
                return redirect(url_for('login_signup.login'))

            if is_user_registered(email):
                flash('This email is already registered. Please use a different email or log in with an existing one.', 'error')
                return redirect(url_for('login_signup.login'))
            else:
                # Encrypt the password before storing it
                hashed_password = hash_password(password)
                unique_id = random.randint(100000, 999999)
                global otp
                otp = random.randint(100000, 999999)

                # Store user registration data in a session for verification
                session['registration_data'] = {
                    'first_name': first_name,
                    'middle_name': middle_name,
                    'last_name': last_name,
                    'email': email,
                    'password': hashed_password,
                    'confirm_password': confirm_password,
                    'year': year,
                    'unique_id': unique_id,
                    'mobile_number': mobile_number,
                    'user': 'New User'
                }

                send_email_verification(email, first_name, otp)

                send_sms(mobile_number, otp)

                return render_template('Homepage/email_verify.html', email=email)
        flash('This email is already registered. Please use a different email or log in with an existing one.', 'error')
        return render_template('Homepage/login.html', language=language, multilingual_content=multilingual_content)

    # ---------------------------- Check if User is already Registered ---------------------
    def is_user_registered(email):  # ---------------- CHECK IF EMAIL IS IN THE DATABASE
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect()
        sql = "SELECT verified FROM signup WHERE email = %s"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        return result

    # -----------------------------Hash Password ----------------------
    def hash_password(password):
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    # -------------------------- Send Email Verification OTP ---------------
    def send_email_verification(email, first_name, otp):
        # Check if API key is set
        if not app.config['ZEPTOMAIL_API_KEY']:
            raise ValueError("ZeptoMail API key is missing. Set it in the environment variables.")

        msg_body = f'''
                   <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OTP</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link
            href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800&display=swap"
            rel="stylesheet">
    </head>
    <body style="font-family: 'Poppins', sans-serif;">
        <link
        href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800&display=swap"
        rel="stylesheet">

        <table align="center" border="0" cellpadding="0" cellspacing="0" width="550" bgcolor="white"
            style="border:2px solid  #660000; border-radius: 5px; box-shadow: 5px 15px 30px #6666; font-family: 'Poppins', sans-serif;">
            <tbody>
                <tr>
                    <td align="center">
                        <table align="center" border="0" cellpadding="0" cellspacing="0" class="col-550" width="550">
                            <tbody>
                                <tr>
                                    <td align="center" style="background-color:  #660000;
                                    height: 50px; border-bottom: 2px solid #660000; border-radius: 5px 5px 0px 0;">

                                        <a href="#" style="text-decoration: none;">
                                            <p style="color:#ffff;
                                           font-weight:bold;font-size: 20px; text-transform: uppercase; ">
                                                Verify Email
                                            </p>
                                        </a>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
                <tr style="height: 300px; background: #fff;">
                    <td align="center" style="border: none;
                    border-bottom: 2px solid #660000; 
                    padding-right: 20px;padding-left:20px;  padding: 30px;">
                        <img src="https://fellowship.trti-maha.in/static/assets/img/tick_animation.gif" width="60px" height="60px" alt="Tick mark">
                        <p style="font-weight: bolder;font-size: 22px;
                       letter-spacing: 0.025em;
                       color:#660000;">
                            Dear, {first_name}
                            <br>
                            Thank you for your interest in creating a user account for Online Fellowship Portal.
                            <br>
                            To activate your account, please enter OTP to the portal.
                        </p>
                        <p
                            style="border: 1px solid transparent; padding: 15px 35px; width: fit-content;  text-align: center; border-radius: 8px; font-weight: bold; background: #660000; color:#fff; letter-spacing: 10px;">
                            {otp}
                        </p>
                    </td>
                </tr>

                <tr style="display: inline-block; width: 100%;">
                    <td style="height: 150px;
                    padding: 20px;
                    border: none; 
                    width: 10%;
                    border-bottom: 2px solid transparent;
                    border-radius: 0px 0px 5px 5px;
                    background-color: #ffff; ">

                        <h2 style="text-align: left;
                        align-items: center; color: #660000;">
                            This OTP will expire in 10 minutes
                        </h2>
                        <p class="data" style="text-align: justify-all;
                       align-items: center; 
                       font-size: 15px; color: #660000;">
                            If you did not request a for sign up, no further action is required.
                        </p>
                        <p class="data" style="text-align: justify-all;
                       align-items: center; 
                       font-size: 15px;
                       padding-bottom: 12px; color: #660000;">
                            Thank you,<br>
                            Fellowship,
                        </p>
                    </td>
                </tr>
                <tr style="display: inline-block; width: 100%;">
                    <td style="max-height: 150px;
                    padding: 40px 20px;
                    border: none; 
                    width: 10%;
                    border-top: 1.5px solid #ffff;
                    border-radius: 0px 0px 5px 5px;
                    background-color: #660000; ">

                        <p style="color: #fff; font-size: 13px;">
                            In case of any technical issue while filling online application form, please contact us
                        </p>
                        <a href="#" style="text-decoration: none; color: #660000; padding: 10px 25px; box-shadow: 0 0 10px #fff; border-radius: 5px; background:#fff;">Contact Us</a>
                    </td>
                </tr>
            </tbody>
        </table>

               '''
        payload = {
            "from": {"address": "noreply_fellowship@trti-maha.in"},
            "to": [
                {
                    "email_address": {
                        "address": email,
                        "name": first_name
                    }
                }
            ],
            "subject": "Verify Email",
            "htmlbody": msg_body
        }

        # Headers
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": app.config['ZEPTOMAIL_API_KEY'],
        }

        # Send the request
        response = requests.post(app.config['ZEPTOMAIL_URL'], json=payload, headers=headers)

    # -------------------------- Send SMS ----------------------------------
    def send_sms(mobile_number, otp):
        authkey = '413185AKlf5Kpy87NZ6597e17fP1'
        sender = 'MHTRTI'
        route = '4'
        country = '91'
        DLT_TE_ID = '1207171690915170968'

        message = f"One Time Password for Fellowship Registration is ({otp}) use only once. Please do not share with anyone. MHTRTI Pune."
        # encoded_message = urllib3.parse.quote(message)

        sms_url = f"https://login.wishbysms.com/api/sendhttp.php?authkey={authkey}&mobiles={mobile_number}&message=Your One Time Password for Fellowship Registration is {otp} use only once. Please do not share with anyone. MHTRTI Pune.I - C - O N COMPUTER&sender={sender}&route={route}&country={country}&DLT_TE_ID={DLT_TE_ID}"
        print(sms_url)

        try:
            response = requests.get(sms_url, verify=True)
            if response.status_code == 200:
                print(f"SMS sent successfully to {mobile_number}")
                return 'SMS sent successfully!'
            else:
                print(f"Error sending SMS to {mobile_number}. Status code: {response.status_code}")
                return f"Error sending SMS. Status code: {response.status_code}"
        except Exception as e:
            print(f"Error sending SMS: {str(e)}")
            return f"Error: {str(e)}"

    # -------------------------- Enter Data into Database ----------------------------
    def insert_user_data(registration_data):
        try:
            host = HostConfig.host
            connect_param = ConnectParam(host)
            cnx, cursor = connect_param.connect()

            # Define your INSERT SQL statement with %s placeholders
            sql = "INSERT INTO signup (first_name, middle_name, last_name, email, password, confirm_password, year, mobile_number, unique_id, user) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            # Extract the data from the 'registration_data' dictionary
            data = (
                registration_data['first_name'],
                registration_data['middle_name'],
                registration_data['last_name'],
                registration_data['email'],
                registration_data['password'],
                registration_data['confirm_password'],
                registration_data['year'],
                registration_data['mobile_number'],
                registration_data['unique_id'],
                registration_data['user']
            )

            # Execute the SQL statement with the data
            cursor.execute(sql, data)

            # Commit the changes to the database
            cnx.commit()

            # Close the cursor and database connection
            cursor.close()
            cnx.close()

            return True  # Return True to indicate a successful insertion

        except mysql.connector.Error as err:
            print("MySQL Error: {}".format(err))
            return False  # Return False to indicate an error occurred during insertion

    # ---------------------------- EMAIL Verfication Route ----------------------------
    @login_blueprint.route('/email_verify', methods=['GET', 'POST'])
    def email_verify():
        if 'registration_data' not in session:
            flash('Session data not found. Please sign up again.', 'error')
            return redirect(url_for('login_signup.signup'))

        user_otp = request.form['otp']

        if otp == int(user_otp):
            registration_data = session.get('registration_data')
            insert_user_data(registration_data)
            flash('Your email is verified and registration is successful.', 'success')
            return redirect(url_for('login_signup.login'))
        else:
            flash('You have entered the wrong OTP. Please enter the OTP again sent to your email', 'error')
            return render_template('Homepage/email_verify.html')
    # ---------------------------------
    #         END SIGN UP ROUTE
    # ---------------------------------

