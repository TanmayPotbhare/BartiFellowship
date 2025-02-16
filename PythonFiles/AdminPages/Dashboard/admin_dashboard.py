from datetime import timedelta, date, datetime
from classes.database import HostConfig, ConfigPaths, ConnectParam
from openpyxl import Workbook
from io import BytesIO
import io
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, jsonify, make_response
from PythonFiles.AdminPages.Dashboard.dashboardCount_functions import *
from PythonFiles.AdminPages.Dashboard.export_column_names import COMMON_COLUMNS, COMMON_HEADERS

admin_dashboard_blueprint = Blueprint('admin_dashboard', __name__)


def admin_dashboard_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    # ----------------------------------------------------------------
    # Fetching Year and different data on Admin Dashboard
    # ----------------------------------------------------------------
    @admin_dashboard_blueprint.route('/get_year_count', methods=['GET', 'POST'])
    def get_year_count():
        """
            This function is used for giving dynamic count on the change of Year on Admin Dashboard.
            This AJAX Call is written in /static/admin.js file on line number 69.
        :return:
        """
        year = request.args.get('year', '2023')
        try:
            data = {
                'total_appl_count': total_application_count(year),
                'completed_form_count': completed_applications(year),
                'incomplete_form_count': incomplete_applications(year),
                'accepted_appl_count': accepted_applications(year),
                'rejected_appl_count': rejected_applications(year),
                'male_count': male_applications(year),
                'female_count': female_applications(year),
                'disabled_count': disabled_applications(year),
                'not_disabled_count': notdisabled_applications(year)
            }
            science_count, arts_count, commerce_count, other_count = get_individual_counts_faculty(year)# Add faculty counts to the data
            data['faculty_counts'] = {
                'science': science_count,
                'arts': arts_count,
                'commerce': commerce_count,
                'other': other_count
            }

            return jsonify(data)
        except Exception as e:
            print(f"Error fetching year count data: {e}")
            return jsonify({"error": "Failed to fetch data"}), 500

    @admin_dashboard_blueprint.route('/get_gender_data', methods=['GET'])
    def get_gender_data():
        """
            This function is used for giving dynamic gender count on the change of Year on Admin Dashboard.
            This AJAX Call is written in /templates/admin_dashboard.html file on line number 315.
        :return:
        """
        data = {
            'male_count': {year: male_applications(year) for year in range(2020, 2024)},
            'female_count': {year: female_applications(year) for year in range(2020, 2024)},
        }
        return jsonify(data)

    @admin_dashboard_blueprint.route('/get_faculty_data', methods=['GET'])
    def get_faculty_data():
        """
            This function is used for giving dynamic gender count on the change of Year on Admin Dashboard.
            This AJAX Call is written in /templates/admin_dashboard.html file on line number 315.
        :return:
        """
        years = range(2020, 2024)
        data = {
            year: {
                'science': get_individual_counts_faculty(year)[0],  # Science count
                'arts': get_individual_counts_faculty(year)[1],  # Arts count
                'commerce': get_individual_counts_faculty(year)[2],  # Commerce count
                'other': get_individual_counts_faculty(year)[3]  # Other count
            }
            for year in years
        }
        return jsonify(data)

    @admin_dashboard_blueprint.route('/get_disabled_data', methods=['GET'])
    def get_disabled_data():
        """
            This function is used for giving dynamic disability count on the change of Year on Admin Dashboard.
            This AJAX Call is written in /templates/admin_dashboard.html file on line number 481.
        :return:
        """
        data = {
            'disabled_count': {year: disabled_applications(year) for year in range(2020, 2024)},
            'not_disabled_count': {year: notdisabled_applications(year) for year in range(2020, 2024)},
        }
        return jsonify(data)

    @admin_dashboard_blueprint.route('/get_district_data', methods=['POST'])
    def get_district_data():
        """
            This function is used for giving dynamic gender count on the change of Year on Admin Dashboard.
            This AJAX Call is written in /templates/admin_dashboard.html file on line number 202.
        :return:
        """
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect()

        # Get the year from the request
        selected_year = request.form['selected_year']

        # Queries to get district data for the map
        district_query = """SELECT district, COUNT(*) AS student_count 
                                            FROM application_page 
                                            WHERE phd_registration_year = %s 
                                            GROUP BY district;"""
        # Execute district count query
        cursor.execute(district_query, (selected_year,))
        district_results = cursor.fetchall()

        # Construct district data dictionary
        district_data = {row[0]: row[1] for row in district_results}  # row[0] is district, row[1] is student_count

        return jsonify(district_data=district_data)

    # END Fetching Year and different data on Admin Dashboard
    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # START Admin Dashboard Route where the functions are written in dashboardCount.py
    # ----------------------------------------------------------------
    @admin_dashboard_blueprint.route('/admin_dashboard', methods=['GET', 'POST'])
    def admin_dashboard():
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            flash('Please enter Email ID and Password', 'error')
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

        # year_selected = "2021" if (role == "Admin" and admin_username == "Admin2021" and admin_year == "BANRF 2021") else None
        year_selected = None

        # if (role == "Admin" and admin_username == "Admin2021" and admin_year == "BANRF 2021"):
        #     year_selected = "2021"
        # elif (role == "Admin" and admin_username == "Admin2022" and admin_year == "BANRF 2022"):
        #     year_selected = "2022"
        # elif (role == "Admin" and admin_username == "Admin2023" and admin_year == "BANRF 2023"):
        #     year_selected = "2023"
        # elif (role == "Admin" and admin_username == "Admin2024" and admin_year == "BANRF 2024"):
        #     year_selected = "2024"

        if (role == "Admin" and admin_username == "Admin2021" and admin_year == "BANRF 2021"):
            year_selected = "2021"
        elif (role == "Admin" and admin_username == "Admin2022" and admin_year == "BANRF 2022"):
            year_selected = "2022"
        elif (role == "Admin" and admin_username == "Admin2023" and admin_year == "BANRF 2023"):
            year_selected = "2023"
        elif (role == "Admin" and admin_username == "Admin2024" and admin_year == "BANRF.2024"):  # corrected typo here
            year_selected = "2024"

        years = ["2020", "2021", "2022", "2023", "2024"]
        year = request.args.get('year', year_selected)
        
        # print("The Dashboard is displayed for year " + year)
        # Try-catch to catch any errors while fetching data

        data = {
            'total_appl_count': total_application_count(year),
            'completed_form_count': completed_applications(year),
            'incomplete_form_count': incomplete_applications(year),
            'accepted_appl_count': accepted_applications(year),
            'rejected_appl_count': rejected_applications(year),
            'male_count': male_applications(year),
            'female_count': female_applications(year),
            'pvtg_applications': pvtg_applications(),
            'disabled_count': disabled_applications(year),
            'not_disabled_count': notdisabled_applications(year)
        }

        katkari, kolam, madia = get_individual_counts_pvtg()  # Use the function you created earlier
        counts = {'katkari': katkari, 'kolam': kolam, 'madia': madia}

        science, arts, commerce, other = get_individual_counts_faculty(year)  # Use the function you created earlier
        faculty_counts = {'science': science, 'arts': arts, 'commerce': commerce, 'other': other}

        cursor.execute("SELECT * FROM admin WHERE username = %s", (user,))
        result = cursor.fetchone()
        cnx.commit()
        cursor.close()
        cnx.close()

        admin_year = result['year']
        admin_username = result['username']
        role = result['role']

        if role == 'Admin':
            first_name = result['first_name'] or ''
            surname = result['surname'] or ''
            username = first_name + ' ' + surname
            if username in ('None', ''):
                username = 'Admin'
        else:
            first_name = result['first_name']
            surname = result['surname']
            username = first_name + ' ' + surname

        return render_template('AdminPages/admin_dashboard.html', data=data, counts=counts,
                               faculty_counts=faculty_counts, username=username, 
                               admin_year=admin_year,year_selected=year_selected,admin_username=admin_username,
                               years=years)

    # END Admin Dashboard
    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # These are reports which consists of records which are redirected form Admin Dashboard.
    # ----------------------------------------------------------------
    @admin_dashboard_blueprint.route('/total_application_report', methods=['GET', 'POST'])
    def total_application_report():
        """
            This function is responsible for handling the dynamic fetching of application report data based
            on the selected year.
            Path of AJAX Call: /static/admin.js file on LINE 139.
            Path of HTML can be found in the render template of this function.
        :return:
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            flash('Please enter Email ID and Password', 'error')
            return redirect(url_for('adminlogin.admin_login'))

        user = session['user']
        print("The user is " + user)
        host = HostConfig.host
        connect_param = ConnectParam(host)

        # Establish database connection
        cnx, cursor = connect_param.connect(use_dict=True)

        try:
            # Fetch admin details
            cursor.execute("SELECT * FROM admin WHERE username = %s", (user,))
            admin_result = cursor.fetchone()

            # Default year selection
            year_selected = "2023"  

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

            print("I am displaying TOTAL applications Report")

            # Get year from request, fallback to admin's assigned year if not provided
            year = request.args.get('year', year_selected)
            print("The year selected is :" +year)

            # Fetch application data based on the selected year
            cursor.execute("SELECT * FROM application_page WHERE phd_registration_year = %s", (year,))
            result = cursor.fetchall()

            # If it's an AJAX request, return JSON response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                for record in result:
                    for key, value in record.items():
                        if isinstance(value, timedelta):
                            record[key] = str(value)  # Convert timedelta to string
                        if isinstance(value, date):
                            record[key] = value.strftime('%Y-%m-%d')  # Format date for JSON
                return jsonify(result)


            # Render template with results
            return render_template(
                'AdminPages/DashboardCountReports/total_application_report.html',
                result=result,
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
            return redirect(url_for('admin_dashboard.total_application_report'))

        finally:
            # Ensure the cursor and connection are closed properly
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()

    @admin_dashboard_blueprint.route('/completed_form', methods=['GET', 'POST'])
    def completed_form():
        """
            This function is responsible for handling the dynamic fetching of application report data based
            on the selected year.
            Path of AJAX Call: /static/admin.js file on LINE 217.
            Path of HTML can be found in the render template of this function.
        :return:
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            flash('Please enter Email ID and Password', 'error')
            return redirect(url_for('adminlogin.admin_login'))
        
        user = session['user']
        print("The user is " + user)
        host = HostConfig.host
        connect_param = ConnectParam(host)

        # Establish database connection
        cnx, cursor = connect_param.connect(use_dict=True)

        try:
            # Fetch admin details
            cursor.execute("SELECT * FROM admin WHERE username = %s", (user,))
            admin_result = cursor.fetchone()

            # Default year selection
            year_selected = "2023"  

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

            print("I am displaying COMPLETED Application Report")

            # Get year from request, fallback to admin's assigned year if not provided
            year = request.args.get('year', year_selected)
            print("The year selected is :" +year)

            # Fetch application data based on the selected year
            cursor.execute("SELECT * FROM application_page WHERE phd_registration_year = %s and form_filled='1' ", (year,))
            result = cursor.fetchall()

            # If it's an AJAX request, return JSON response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                for record in result:
                    for key, value in record.items():
                        if isinstance(value, timedelta):
                            record[key] = str(value)  # Convert timedelta to string
                        if isinstance(value, date):
                            record[key] = value.strftime('%Y-%m-%d')  # Format date for JSON
                return jsonify(result)


            # Render template with results
            return render_template(
                'AdminPages/DashboardCountReports/completed_form.html',
                result=result,
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
            return redirect(url_for('admin_dashboard.completed_form'))

        finally:
            # Ensure the cursor and connection are closed properly
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()

    @admin_dashboard_blueprint.route('/incompleted_form', methods=['GET', 'POST'])
    def incompleted_form():
        """
            This function is responsible for handling the dynamic fetching of application report data based
            on the selected year.
            Path of AJAX Call: /static/admin.js file on LINE 296.
            Path of HTML can be found in the render template of this function.
        :return:
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            flash('Please enter Email ID and Password', 'error')
            return redirect(url_for('adminlogin.admin_login'))
        
        user = session['user']
        print("The user is " + user)
        host = HostConfig.host
        connect_param = ConnectParam(host)

        # Establish database connection
        cnx, cursor = connect_param.connect(use_dict=True)

        try:
            # Fetch admin details
            cursor.execute("SELECT * FROM admin WHERE username = %s", (user,))
            admin_result = cursor.fetchone()

            # Default year selection
            year_selected = "2023"  

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

            print("I am displaying INCOMPLETE Application Completed Report")

            # Get year from request, fallback to admin's assigned year if not provided
            year = request.args.get('year', year_selected)
            print("The year selected is :" +year)

            # Fetch application data based on the selected year
            cursor.execute("SELECT * FROM application_page WHERE phd_registration_year = %s and form_filled='0' ", (year,))
            result = cursor.fetchall()

            # If it's an AJAX request, return JSON response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                for record in result:
                    for key, value in record.items():
                        if isinstance(value, timedelta):
                            record[key] = str(value)  # Convert timedelta to string
                        if isinstance(value, date):
                            record[key] = value.strftime('%Y-%m-%d')  # Format date for JSON
                return jsonify(result)


            # Render template with results
            return render_template(
                'AdminPages/DashboardCountReports/incompleted_form.html',
                result=result,
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
            return redirect(url_for('admin_dashboard.incompleted_form'))

        finally:
            # Ensure the cursor and connection are closed properly
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()

    @admin_dashboard_blueprint.route('/total_accepted_report', methods=['GET', 'POST'])
    def total_accepted_report():
        """
            This function is responsible for handling the dynamic fetching of application report data based
            on the selected year.
            Path of AJAX Call: /static/admin.js file on LINE 374.
            Path of HTML can be found in the render template of this function.
        :return:
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            flash('Please enter Email ID and Password', 'error')
            return redirect(url_for('adminlogin.admin_login'))

        user = session['user']
        print("The user is " + user)
        host = HostConfig.host
        connect_param = ConnectParam(host)

        # Establish database connection
        cnx, cursor = connect_param.connect(use_dict=True)

        try:
            # Fetch admin details
            cursor.execute("SELECT * FROM admin WHERE username = %s", (user,))
            admin_result = cursor.fetchone()

            # Default year selection
            year_selected = "2023"  

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

            print("I am displaying Total ACCEPTED Application Report")

            # Get year from request, fallback to admin's assigned year if not provided
            year = request.args.get('year', year_selected)
            print("The year selected is :" +year)

            # Fetch application data based on the selected year
            cursor.execute("SELECT * FROM application_page WHERE phd_registration_year = %s and form_filled='1' and final_approval='accepted' ", (year,))
            result = cursor.fetchall()

            # If it's an AJAX request, return JSON response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                for record in result:
                    for key, value in record.items():
                        if isinstance(value, timedelta):
                            record[key] = str(value)  # Convert timedelta to string
                        if isinstance(value, date):
                            record[key] = value.strftime('%Y-%m-%d')  # Format date for JSON
                return jsonify(result)


            # Render template with results
            return render_template(
                'AdminPages/DashboardCountReports/total_accepted_report.html',
                result=result,
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
            return redirect(url_for('admin_dashboard.total_accepted_report'))

        finally:
            # Ensure the cursor and connection are closed properly
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()    

    @admin_dashboard_blueprint.route('/total_rejected_report', methods=['GET', 'POST'])
    def total_rejected_report():
        """
            This function is responsible for handling the dynamic fetching of application report data based
            on the selected year.
            Path of AJAX Call: /static/admin.js file on LINE 452.
            Path of HTML can be found in the render template of this function.
        :return:
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            flash('Please enter Email ID and Password', 'error')
            return redirect(url_for('adminlogin.admin_login'))
        
        user = session['user']
        print("The user is " + user)
        host = HostConfig.host
        connect_param = ConnectParam(host)

        # Establish database connection
        cnx, cursor = connect_param.connect(use_dict=True)

        try:
            # Fetch admin details
            cursor.execute("SELECT * FROM admin WHERE username = %s", (user,))
            admin_result = cursor.fetchone()

            # Default year selection
            year_selected = "2023"  

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

            print("I am displaying Total REJECTED Application Report")

            # Get year from request, fallback to admin's assigned year if not provided
            year = request.args.get('year', year_selected)
            print("The year selected is :" +year)

            # Fetch application data based on the selected year
            cursor.execute("SELECT * FROM application_page WHERE phd_registration_year = %s and form_filled='1' and final_approval='rejected' ", (year,))
            result = cursor.fetchall()

            # If it's an AJAX request, return JSON response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                for record in result:
                    for key, value in record.items():
                        if isinstance(value, timedelta):
                            record[key] = str(value)  # Convert timedelta to string
                        if isinstance(value, date):
                            record[key] = value.strftime('%Y-%m-%d')  # Format date for JSON
                return jsonify(result)


            # Render template with results
            return render_template(
                'AdminPages/DashboardCountReports/total_rejected_report.html',
                result=result,
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
            return redirect(url_for('admin_dashboard.total_rejected_report'))

        finally:
            # Ensure the cursor and connection are closed properly
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()    

    @admin_dashboard_blueprint.route('/male_report', methods=['GET', 'POST'])
    def male_report():
        """
            This function is responsible for handling the dynamic fetching of application report data based
            on the selected year.
            Path of AJAX Call: /static/admin.js file on LINE 530.
            Path of HTML can be found in the render template of this function.
        :return:
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            flash('Please enter Email ID and Password', 'error')
            return redirect(url_for('adminlogin.admin_login'))
        
        user = session['user']
        print("The user is " + user)
        host = HostConfig.host
        connect_param = ConnectParam(host)

        # Establish database connection
        cnx, cursor = connect_param.connect(use_dict=True)

        try:
            # Fetch admin details
            cursor.execute("SELECT * FROM admin WHERE username = %s", (user,))
            admin_result = cursor.fetchone()

            # Default year selection
            year_selected = "2023"  

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

            print("I am displaying Total MALE Application Report")

            # Get year from request, fallback to admin's assigned year if not provided
            year = request.args.get('year', year_selected)
            print("The year selected is :" +year)

            # Fetch application data based on the selected year
            cursor.execute("SELECT * FROM application_page WHERE phd_registration_year = %s and gender='Male' ", (year,))
            result = cursor.fetchall()

            # If it's an AJAX request, return JSON response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                for record in result:
                    for key, value in record.items():
                        if isinstance(value, timedelta):
                            record[key] = str(value)  # Convert timedelta to string
                        if isinstance(value, date):
                            record[key] = value.strftime('%Y-%m-%d')  # Format date for JSON
                return jsonify(result)


            # Render template with results
            return render_template(
                'AdminPages/DashboardCountReports/male_report.html',
                result=result,
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
            return redirect(url_for('admin_dashboard.male_report'))

        finally:
            # Ensure the cursor and connection are closed properly
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()    

    @admin_dashboard_blueprint.route('/female_report', methods=['GET', 'POST'])
    def female_report():
        """
            This function is responsible for handling the dynamic fetching of application report data based
            on the selected year.
            Path of AJAX Call: /static/admin.js file on LINE 615.
            Path of HTML can be found in the render template of this function.
        :return:
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            flash('Please enter Email ID and Password', 'error')
            return redirect(url_for('adminlogin.admin_login'))
        
        user = session['user']
        print("The user is " + user)
        host = HostConfig.host
        connect_param = ConnectParam(host)

        # Establish database connection
        cnx, cursor = connect_param.connect(use_dict=True)

        try:
            # Fetch admin details
            cursor.execute("SELECT * FROM admin WHERE username = %s", (user,))
            admin_result = cursor.fetchone()

            # Default year selection
            year_selected = "2023"  

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

            
            print("I am displaying Total FEMALE Application Report")

            # Get year from request, fallback to admin's assigned year if not provided
            year = request.args.get('year', year_selected)
            print("The year selected is :" +year)

            # Fetch application data based on the selected year
            cursor.execute("SELECT * FROM application_page WHERE phd_registration_year = %s and gender='Female' ", (year,))
            result = cursor.fetchall()

            # If it's an AJAX request, return JSON response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                for record in result:
                    for key, value in record.items():
                        if isinstance(value, timedelta):
                            record[key] = str(value)  # Convert timedelta to string
                        if isinstance(value, date):
                            record[key] = value.strftime('%Y-%m-%d')  # Format date for JSON
                return jsonify(result)


            # Render template with results
            return render_template(
                'AdminPages/DashboardCountReports/female_report.html',
                result=result,
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
            return redirect(url_for('admin_dashboard.female_report'))

        finally:
            # Ensure the cursor and connection are closed properly
            if cursor:
                cursor.close()
            if cnx:
                cnx.close() 

    @admin_dashboard_blueprint.route('/disabled_report', methods=['GET', 'POST'])
    def disabled_report():
        """
            This function is responsible for handling the dynamic fetching of application report data based
            on the selected year.
            Path of AJAX Call: /static/admin.js file on LINE 615.
            Path of HTML can be found in the render template of this function.
        :return:
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            flash('Please enter Email ID and Password', 'error')
            return redirect(url_for('adminlogin.admin_login'))
                
        user = session['user']
        print("The user is " + user)
        host = HostConfig.host
        connect_param = ConnectParam(host)

        # Establish database connection
        cnx, cursor = connect_param.connect(use_dict=True)

        try:
            # Fetch admin details
            cursor.execute("SELECT * FROM admin WHERE username = %s", (user,))
            admin_result = cursor.fetchone()

            # Default year selection
            year_selected = "2023"  

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

            print("I am displaying Total DISABLED Application Report")

            # Get year from request, fallback to admin's assigned year if not provided
            year = request.args.get('year', year_selected)
            print("The year selected is :" +year)

            # Fetch application data based on the selected year
            cursor.execute("SELECT * FROM application_page WHERE phd_registration_year = %s and disability='Yes' ", (year,))
            result = cursor.fetchall()

            # If it's an AJAX request, return JSON response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                for record in result:
                    for key, value in record.items():
                        if isinstance(value, timedelta):
                            record[key] = str(value)  # Convert timedelta to string
                        if isinstance(value, date):
                            record[key] = value.strftime('%Y-%m-%d')  # Format date for JSON
                return jsonify(result)


            # Render template with results
            return render_template(
                'AdminPages/DashboardCountReports/disabled_report.html',
                result=result,
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
            return redirect(url_for('admin_dashboard.disabled_report'))

        finally:
            # Ensure the cursor and connection are closed properly
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()     

    @admin_dashboard_blueprint.route('/not_disabled_report', methods=['GET', 'POST'])
    def not_disabled_report():
        """
            This function is responsible for handling the dynamic fetching of application report data based
            on the selected year.
            Path of AJAX Call: /static/admin.js file on LINE 615.
            Path of HTML can be found in the render template of this function.
        :return:
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            flash('Please enter Email ID and Password', 'error')
            return redirect(url_for('adminlogin.admin_login'))


        user = session['user']
        print("The user is " + user)
        host = HostConfig.host
        connect_param = ConnectParam(host)

        # Establish database connection
        cnx, cursor = connect_param.connect(use_dict=True)

        try:
            # Fetch admin details
            cursor.execute("SELECT * FROM admin WHERE username = %s", (user,))
            admin_result = cursor.fetchone()

            # Default year selection
            year_selected = "2023"  

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

            print("I am displaying Total NOT DISABLED Application Report")

            # Get year from request, fallback to admin's assigned year if not provided
            year = request.args.get('year', year_selected)
            print("The year selected is :" +year)

            # Fetch application data based on the selected year
            cursor.execute("SELECT * FROM application_page WHERE phd_registration_year = %s and disability='No' ", (year,))
            result = cursor.fetchall()

            # If it's an AJAX request, return JSON response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                for record in result:
                    for key, value in record.items():
                        if isinstance(value, timedelta):
                            record[key] = str(value)  # Convert timedelta to string
                        if isinstance(value, date):
                            record[key] = value.strftime('%Y-%m-%d')  # Format date for JSON
                return jsonify(result)


            # Render template with results
            return render_template(
                'AdminPages/DashboardCountReports/not_disabled_report.html',
                result=result,
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
            return redirect(url_for('admin_dashboard.not_disabled_report'))

        finally:
            # Ensure the cursor and connection are closed properly
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()    

    # END Reports
    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # Common Export to Excel Function
    # ----------------------------------------------------------------
    @admin_dashboard_blueprint.route('/export_to_excel', methods=['GET'])
    def export_to_excel():
        """
            This function is responsible for handling the dynamic exporting of application report data based
            on the selected year.
            Path of AJAX Call: /static/admin.js. (Search the form_types in the JS File)
            Path of HTML can be found in the respective templates.
            {columns_str} will be found in: PythonFiles/AdminPages/Dashboard/export_column_names.py
        """
        if not session.get('logged_in'):
            flash('Please enter Email ID and Password', 'error')
            return redirect(url_for('adminlogin.admin_login'))

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        year = request.args.get('year', default=2023, type=int)
        # print(year)
        form_type = request.args.get('form_type')  # Get the form type (e.g., "completed_form")

        columns_str = ', '.join(COMMON_COLUMNS)

        # Dynamically change the SQL query based on form_type
        if form_type == "total_application_records":
            cursor.execute(f"SELECT {columns_str} FROM application_page WHERE phd_registration_year = %s", (year,))
        elif form_type == "completed_form_records":
            cursor.execute(f"SELECT {columns_str} FROM application_page WHERE phd_registration_year = %s AND form_filled='1'",
                           (year,))
        elif form_type == "incomplete_form_records":
            cursor.execute(f"SELECT {columns_str} FROM application_page WHERE phd_registration_year = %s AND form_filled='0'",
                           (year,))
        elif form_type == 'accepted_records':
            cursor.execute(f"SELECT {columns_str} FROM application_page WHERE phd_registration_year = %s AND "
                           "final_approval='accepted' AND form_filled=1 ",
                           (year,))
        elif form_type == 'rejected_records':
            cursor.execute(f"SELECT {columns_str} FROM application_page WHERE phd_registration_year = %s AND "
                           "final_approval='rejected' AND form_filled=1 ",
                           (year,))
        elif form_type == 'male_application_records':
            cursor.execute(f"SELECT {columns_str} FROM application_page WHERE phd_registration_year = %s and gender='Male' ",
                           (year,))
        elif form_type == 'female_application_records':
            cursor.execute(f"SELECT {columns_str} FROM application_page WHERE phd_registration_year = %s and gender='Female' ",
                           (year,))
        elif form_type == 'disabled_application_records':
            cursor.execute(f"SELECT {columns_str} FROM application_page WHERE phd_registration_year = %s and disability='Yes' ",
                           (year,))
        elif form_type == 'not_disabled_application_records':
            cursor.execute(f"SELECT {columns_str} FROM application_page WHERE phd_registration_year = %s and disability='No' ",
                           (year,))
        else:
            # Handle other form types or default case
            flash('Error fetching Details. Some details are missing.', 'error')

        data = cursor.fetchall()  # Fetch the results

        # Close the connection
        cursor.close()
        cnx.close()

        # Create an Excel workbook
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = f"Data_{year}"

        # Write headers
        if data:
            # Map database column names to headers
            headers = [COMMON_HEADERS.get(column, column) for column in
                       data[0].keys()]  # Use COMMON_HEADERS for headers
            sheet.append(headers)  # Add headers to the first row

            # Write data rows
            for row_data in data:
                sheet.append(
                    [row_data.get(column, '') for column in data[0].keys()])  # Ensure data matches the header order

        # Save the workbook to an in-memory stream
        output = BytesIO()
        workbook.save(output)
        output.seek(0)

        # Return the file as a downloadable response
        response = make_response(output.read())
        response.headers['Content-Disposition'] = f'attachment; filename=export_{form_type}_{year}.xlsx'
        response.headers['Content-type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        return response

    # END Common Export to Excel
    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # START Add, View, Update, Delete Admin Function
    # ----------------------------------------------------------------
    @admin_dashboard_blueprint.route('/addAdmin', methods=['GET', 'POST'])
    def addAdmin():
        """
            This function is responsible for handling the dynamic exporting of application report data based
            on the selected year.
            Path of AJAX Call: /static/admin.js. (Search the form_types in the JS File)
            Path of HTML can be found in the respective templates.
            {columns_str} will be found in: PythonFiles/AdminPages/Dashboard/export_column_names.py
        """

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute("SELECT * FROM admin WHERE role = 'Admin'")
        record = cursor.fetchall()

        cursor.execute("SELECT username FROM admin WHERE role = 'Admin'")
        existing_usernames = [row['username'] for row in cursor.fetchall()]
        # print(existing_usernames)

        cursor.execute("SELECT year FROM admin WHERE role = 'Admin'")
        existing_years = [row['year'] for row in cursor.fetchall()]
        # print(existing_years)

        cnx.commit()
        cursor.close()
        cnx.close()
        return render_template('AdminPages/addAdmin.html', record=record,existing_usernames=existing_usernames,
                               existing_years=existing_years)

    @admin_dashboard_blueprint.route('/addAdmin_submit', methods=['GET', 'POST'])
    def addAdmin_submit():
        """
            This function is responsible for submitting the ADD Admin Form in Add User Functionality for Admin Master 
            in HoD Login
        """
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        if request.method == 'POST':
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            last_name = request.form['last_name']
            mobile_number = request.form['mobile_number']
            age = request.form['age']
            dob = request.form['date_of_birth']
            email = request.form['email']
            password = request.form['password']
            gender = request.form['gender']
            role = request.form['role']
            year = request.form['year']
            username = request.form['username']

            cursor.execute("SELECT * FROM admin WHERE email = %s", (email,))
            record = cursor.fetchone()

            if is_user_already_exist(username):
                flash('An admin is already registered for this year. Please select a different year.', 'info')
                return redirect(url_for('admin_dashboard.addAdmin'))

            if record:
                flash('Admin already exists. Please update the details if necessary.', 'info')
                return redirect(url_for('admin_dashboard.addAdmin'))
            else:
                added_date = datetime.now().date()
                added_time = datetime.now().time()
                added_by = 'HoD'
                # role = 'Admin'

                cursor.execute(
                    "INSERT INTO admin (first_name, middle_name, surname, mobile_number, age, dob, email, "
                    " username, password, gender, added_date, added_time, added_by, role, year) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (first_name, middle_name, last_name, mobile_number, age, dob, email, username, password, gender,
                     added_date, added_time, added_by, role, year))
                cnx.commit()

                flash('Admin Added successfully and Mail has been sent with the credentials', 'success')
                return redirect(url_for('admin_dashboard.addAdmin'))
        return render_template('AdminPages/addAdmin.html')

    @admin_dashboard_blueprint.route('/delete_admin/<int:id>')
    def delete_admin(id):
        """
            This function is responsible for DELETE ADMIN functionality for Admin Master in HOD Login
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('adminlogin.admin_login'))

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        try:
            sql = "DELETE FROM admin WHERE id = %s"
            cursor.execute(sql, (id,))
            cnx.commit() 

            flash('Admin Deleted Successfully!', 'success') 

        except Exception as e:
            print(f"Error deleting admin: {e}")
            flash('An error occurred while deleting the admin.', 'error')

        finally:
            cursor.close()
            cnx.close()

        return redirect(url_for('admin_dashboard.addAdmin'))

    @admin_dashboard_blueprint.route('/edit_admin/<int:id>' , methods=['GET', 'POST'])
    def edit_admin(id):
        """
            This function is responsible for EDIT ADMIN functionality for Admin Master in HOD Login
        """
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)
        admin_id = id
        my_id = str(admin_id)
        print("I am editing rec for Admin with ID " + my_id)
        if request.method == 'POST':
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            last_name = request.form['surname']
            mobile_number = request.form['mobile_number']
            # age = request.form['age']
            # dob = request.form['date_of_birth']
            email = request.form['email']
            # password = request.form['password']
            # gender = request.form['gender']
            role = request.form['role']
            year = request.form['year']
            username = request.form['username']

            cursor.execute("SELECT * FROM admin WHERE email = %s", (email,))
            record = cursor.fetchone()

            # if is_user_already_exist(username):
            #     flash('An admin is already registered for this year. Please select a different year.', 'info')
            #     return redirect(url_for('admin_dashboard.addAdmin'))
            updated_date = datetime.now().date()
            updated_time = datetime.now().time()
            updated_by = 'HoD'
            # role = 'Admin'

            cursor.execute(
                "UPDATE admin SET first_name = %s, middle_name = %s, surname = %s, mobile_number = %s, email = %s, "
                "username = %s, updated_date = %s, updated_time = %s, updated_by = %s, role = %s, year = %s "
                "WHERE id = %s",  # Ensure the WHERE clause specifies the row to update
                (first_name, middle_name, last_name, mobile_number, email, username,
                updated_date, updated_time, updated_by, role, year, admin_id)  # Pass `admin_id` for the WHERE condition
            )
            cnx.commit()
            flash('Admin Updated successfully !!', 'success')
            return redirect(url_for('admin_dashboard.addAdmin'))
        return render_template('AdminPages/addAdmin.html')

    # END Add, View, Update, Delete Admin Function
    # ----------------------------------------------------------------

    @admin_dashboard_blueprint.route('/view_candidate/<int:id>')
    def view_candidate(id):
        """
            This function is used to display the records of users after logging in. This is the first page
            which is shown to the user and consists of conditioning of sidebar according to the status of fellowship.
        """
        # email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """SELECT * FROM application_page WHERE id = %s"""
        cursor.execute(sql, (id,))
        records = cursor.fetchone()
        print(records)
        # Check if the user is approved for fellowship no matter the year to show the desired sidebar.
        if records['final_approval'] == 'accepted':
            finally_approved = 'approved'
        else:
            finally_approved = 'pending'

        # Pass the user and Photo to the header and the template to render is neatly instead of keeping it in session.
        if records:
            user = records['first_name'] + ' ' + records['last_name']
            photo = records['applicant_photo']
        else:
            user = "Admin"
            photo = '/static/assets/img/default_user.png'

        # Convert the Date to standard Format
        first_record = records
        DoB = first_record['date_of_birth'] # Date of Birth
        formatted_date_of_birth = DoB.strftime('%d-%b-%Y')   
 
        application_date = first_record['application_date'] # Application Date
        formatted_application_date = application_date.strftime('%d-%b-%Y')

        PHD_reg_date = first_record['phd_registration_date'] # PHD Registration Date
        formatted_PHD_reg_date = PHD_reg_date.strftime('%d-%b-%Y')

        return render_template('AdminPages/view_candidate.html', title="My Profile", records=records,
                               user=user, photo=photo, finally_approved=finally_approved, 
                               formatted_date_of_birth=formatted_date_of_birth,
                               formatted_application_date=formatted_application_date,
                               formatted_PHD_reg_date=formatted_PHD_reg_date)
    
    # ---------------------------- Check if Admin is already Registered ---------------------
    def is_user_already_exist(username):  # ---------------- CHECK IF Username IS IN THE DATABASE
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect()
        sql = "SELECT username FROM admin WHERE username = %s"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        return result
    

# -------------------------------------------------------------------------------------------------
# -------------------Start VIEW, ADD, EDIT, DELETE functionality for HRA Master----------------------
# -------------------------------------------------------------------------------------------------

# --------------------VIEW HRA Rate---------------------------------------------------------------
    @admin_dashboard_blueprint.route('/hra_master', methods=['GET', 'POST'])
    def hra_master():
        """
            This function is responsible for redirecting to the HRA Master in Admin Login
        """

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute("SELECT * FROM hra_rate_master ")
        record = cursor.fetchall()

        cursor.execute("SELECT city FROM cities ORDER BY city ASC")
        city_list = cursor.fetchall()
        print(city_list)

        cnx.commit()
        cursor.close()
        cnx.close()
        return render_template('AdminPages/hra_master.html', record=record,city_list=city_list)
    
    # --------------------------ADD HRA Rate-----------------------------------
    @admin_dashboard_blueprint.route('/submit_HRA_rate', methods=['GET', 'POST'])
    def submit_HRA_rate():
        """
            This function is responsible for submitting the HRA Rate Form in ADD Rate Functionality for HRA Master
            in HoD Login
        """
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        if request.method == 'POST':
            city = request.form['city']
            rate = request.form['rate']
            category = request.form['category']

            if is_city_already_exist(city):
                flash('HRA Rate is already set for this city. Please Edit the rates for the same.', 'info')
                return redirect(url_for('admin_dashboard.hra_master'))
            
            added_date = datetime.now().date()
            added_time = datetime.now().time()
            added_by = 'HoD'
            # role = 'Admin'

            cursor.execute(
                "INSERT INTO hra_rate_master (city, rate, category, added_date, added_time, added_by) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (city, rate, category, added_date, added_time, added_by))
            cnx.commit()

            flash('HRA Rate added successfully!!', 'success')
            return redirect(url_for('admin_dashboard.hra_master'))
        return render_template('AdminPages/hra_master.html')

    # ---------------------------- Check if city already exists in DB ----------------------
    def is_city_already_exist(city):  # ---------------- CHECK IF city IS IN THE DATABASE
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect()
        sql = "SELECT city FROM hra_rate_master WHERE city = %s"
        cursor.execute(sql, (city,))
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        return result
    
# --------------------------------DELETE HRA Rate-------------------------------------------
    @admin_dashboard_blueprint.route('/delete_hra/<int:id>')
    def delete_hra(id):
        """
            This function is responsible for DELETE HRA Rate functionality for HRA Master in HOD Login
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('adminlogin.admin_login'))

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        try:
            sql = "DELETE FROM hra_rate_master WHERE id = %s"
            cursor.execute(sql, (id,))
            cnx.commit() 

            flash('HRA Rate Deleted Successfully!', 'success') 

        except Exception as e:
            print(f"Error deleting HRA Rate: {e}")
            flash('An error occurred while deleting the admin.', 'error')

        finally:
            cursor.close()
            cnx.close()

        return redirect(url_for('admin_dashboard.hra_master'))

# -------------------------------------------------------------------------------------------------
# -------------------End VIEW, ADD, EDIT, DELETE functionality for HRA Master----------------------
# -------------------------------------------------------------------------------------------------
#     
# -------------------------------------------------------------------------------------------------
# -------------------Start VIEW, ADD, EDIT, DELETE functionality for JRF-SRF Master----------------
# -------------------------------------------------------------------------------------------------

    # -------------------- VIEW JRF-SRF Amount--------------------
    @admin_dashboard_blueprint.route('/jrf_srf_master', methods=['GET', 'POST'])
    def jrf_srf_master():
        """
            This function is responsible for redirecting to the JRF-SRF Master in Admin Login
        """

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute("SELECT * FROM jrf_srf_master ")
        record = cursor.fetchall()

        cnx.commit()
        cursor.close()
        cnx.close()
        return render_template('AdminPages/jrf_srf_master.html', record=record)
    
    # -------------------- ADD JRF-SRF Amount--------------------
    @admin_dashboard_blueprint.route('/submit_jrf_srf', methods=['GET', 'POST'])
    def submit_jrf_srf():
        """
            This function is responsible for submitting the JRF-SRF Rate Form in ADD Amount Functionality for JRF-SRF Master
            in HoD Login
        """
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        if request.method == 'POST':
            jrf_amount = request.form['jrf_amount']
            srf_amount = request.form['srf_amount']
            year = request.form['year']
            added_date = datetime.now().date()
            added_time = datetime.now().time()
            added_by = 'HoD'
            # role = 'Admin'

            cursor.execute(
                "INSERT INTO jrf_srf_master (jrf_amount, srf_amount, year, added_date, added_time, added_by) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (jrf_amount, srf_amount, year, added_date, added_time, added_by))
            cnx.commit()

            flash('JRF/SRF Amount added successfully!!', 'success')
            return redirect(url_for('admin_dashboard.jrf_srf_master'))
        return render_template('AdminPages/jrf_srf_master.html')
    
    # -------------------- DELETE JRF-SRF Amount--------------------
    @admin_dashboard_blueprint.route('/delete_jrf/<int:id>')
    def delete_jrf(id):
        """
            This function is responsible for DELETE JRF/SRF Rate functionality for JRF/SRF Master in HOD Login
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('adminlogin.admin_login'))

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        try:
            sql = "DELETE FROM jrf_srf_master WHERE id = %s"
            cursor.execute(sql, (id,))
            cnx.commit() 

            flash('JRF/SRf Amount Deleted Successfully!', 'success') 

        except Exception as e:
            print(f"Error deleting JRF/SRf Amount: {e}")
            flash('An error occurred while deleting the admin.', 'error')

        finally:
            cursor.close()
            cnx.close()

        return redirect(url_for('admin_dashboard.jrf_srf_master'))
    
# -------------------------------------------------------------------------------------------------
# -------------------End VIEW, ADD, EDIT, DELETE functionality for JRF-SRF Master------------------
# -------------------------------------------------------------------------------------------------    