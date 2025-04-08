from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response
from authentication.middleware import auth
import bcrypt
from flask import jsonify

manage_profile_blueprint = Blueprint('manage_profile', __name__)


def manage_profile_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @manage_profile_blueprint.route('/manage_profile', methods=['GET', 'POST'])
    def manage_profile():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """SELECT * FROM application_page WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchall()

        # Check if the user is approved for fellowship no matter the year to show the desired sidebar.
        if records[0]['final_approval'] == 'accepted':
            finally_approved = 'approved'
        else:
            finally_approved = 'pending'

        # Pass the user and Photo to the header and the template to render is neatly instead of keeping it in session.
        if records:
            user = records[0]['first_name'] + ' ' + records[0]['last_name']
            photo = records[0]['applicant_photo']
        else:
            user = "Admin"
            photo = '/static/assets/img/default_user.png'

        # Convert the Date to standard Format
        first_record = records[0]
        Application_date = first_record['application_date'] # PHD Registration Date
        formatted_Application_date = Application_date.strftime('%d-%b-%Y')

        return render_template('CandidatePages/manage_profile.html', title="Manage Profile", records=records,
                               user=user, photo=photo, finally_approved=finally_approved, formatted_Application_date=formatted_Application_date)


    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    
    @manage_profile_blueprint.route('/change_password_user', methods=['POST'])
    def change_password_user():
        if request.method == 'POST':
            current_password = request.form['current_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            email = session.get('email')

            if not email:
                flash("Session expired. Please log in again.", "error")
                return redirect(url_for('login'))

            # Connect to the database
            host = HostConfig.host
            connect_param = ConnectParam(host)
            cnx, cursor = connect_param.connect(use_dict=True)

            try:
                # Retrieve hashed password from the database
                query = 'SELECT password FROM signup WHERE email = %s'
                cursor.execute(query, (email,))
                result = cursor.fetchone()

                if result:
                    stored_password = result['password']

                    # Check if stored_password is hashed (bcrypt hash starts with "$2")
                    if stored_password.startswith('$2b$') or stored_password.startswith('$2a$'):
                        # Verify hashed password
                        password_matches = bcrypt.checkpw(current_password.encode('utf-8'), stored_password.encode('utf-8'))
                    else:
                        # Compare as plain text
                        password_matches = (current_password == stored_password)

                    if password_matches:
                        if new_password != confirm_password:
                            flash("New Password and Confirm Password do not match.", "error")
                            return redirect(url_for('manage_profile.manage_profile'))

                        # Hash the new password before storing (ensure it's hashed for security)
                        hashed_password = hash_password(new_password).decode('utf-8')

                        # Update password in the database (removing confirm_password field)
                        update_query = 'UPDATE signup SET password = %s, confirm_password = %s WHERE email = %s'
                        cursor.execute(update_query, (hashed_password, confirm_password, email))
                        cnx.commit()

                        flash("Password updated successfully.", "success")
                        return redirect(url_for('candidate_dashboard.candidate_dashboard'))
                    else:
                        flash("Incorrect current password.", "error")
                else:
                    flash("User not found.", "error")

            except Exception as e:
                flash(f"An error occurred: {str(e)}", "error")

            finally:
                cursor.close()
                cnx.close()

            return redirect(url_for('manage_profile.manage_profile'))
        
    @manage_profile_blueprint.route('/check-current-password', methods=['POST'])
    def check_current_password():
        email = session.get('email')

        if not email:
            return jsonify({'valid': False, 'message': 'Session expired. Please log in again.'})

        data = request.get_json()
        current_password = data.get('password')

        # Connect to the database
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        try:
            # Fetch the stored password
            query = 'SELECT password FROM signup WHERE email = %s'
            cursor.execute(query, (email,))
            result = cursor.fetchone()

            # if result:
            #     stored_hashed_password = result['password']

            #     if bcrypt.checkpw(current_password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            #         return jsonify({'valid': True, 'message': 'Current password verified successfully.'})
            #     else:
            #         return jsonify({'valid': False, 'message': 'Incorrect current password.'})
            # else:
            #     return jsonify({'valid': False, 'message': 'User not found.'})
            

            if result:
                stored_password = result['password']

                # Check if stored_password is hashed (bcrypt hash starts with "$2")
                if stored_password.startswith('$2b$') or stored_password.startswith('$2a$'):
                    # Verify using bcrypt
                    if bcrypt.checkpw(current_password.encode('utf-8'), stored_password.encode('utf-8')):
                        return jsonify({'valid': True, 'message': 'Current password verified successfully.'})
                    else:
                        return jsonify({'valid': False, 'message': 'Incorrect current password.'})
                else:
                    # Compare as plain text (not recommended, but needed for legacy cases)
                    if current_password == stored_password:
                        return jsonify({'valid': True, 'message': 'Current password verified successfully.'})
                    else:
                        return jsonify({'valid': False, 'message': 'Incorrect current password.'})
            else:
                return jsonify({'valid': False, 'message': 'User not found.'})
                

        except Exception as e:
            return jsonify({'valid': False, 'message': f'Error: {str(e)}'})

        finally:
            cursor.close()
            cnx.close()