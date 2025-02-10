from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
from classes.database import HostConfig, ConfigPaths, ConnectParam
from PythonFiles.Homepage.multilingual_content import *
import folium
import mysql.connector

homepage_blueprint = Blueprint('homepage', __name__)


def homepage_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    # ---------------------------------
    #           HOMEPAGE
    # ---------------------------------
    @homepage_blueprint.route('/', methods=['GET', 'POST'])
    def home_page():
        """
            This function is the main function which renders when the website is being hit.
        """
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'

        # --------------------------  HOME PAGE
        total_count = applications_today()
        fellow_awarded = fellow_awarded_count()
        total_appl_22 = total_appl_22_count()
        total_appl_23 = total_appl_23_count()

        # print("old user 2022",old_user_22)
        news_record = news_fetch()
        print(news_record)
        return render_template('Homepage/homepage.html', total_count=total_count, fellow_awarded=fellow_awarded,
                               total_appl_22=total_appl_22, total_appl_23=total_appl_23,
                               language=language, multilingual_content=multilingual_content, news_record=news_record)

    def applications_today():
        """
            This function gives the total count of students registered after the year 2022.
        """
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect()
        cursor.execute(" SELECT COUNT(*) FROM application_page where phd_registration_year>=2023 ")
        result = cursor.fetchone()
        print(result)
        return result[0]

    def fellow_awarded_count():
        """
            This function gives the total count of students who are awarded fellowship.
        """
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect()
        cursor.execute(
            " SELECT COUNT(*) FROM application_page where phd_registration_year='2023' and final_approval='accepted' ")
        result = cursor.fetchone()
        print(result)
        return result[0]

    def total_appl_22_count():
        """
            This function gives the total count of students registered for the year 2022.
        """
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect()
        cursor.execute(" SELECT COUNT(*) FROM application_page where phd_registration_year='2022' ")
        result = cursor.fetchone()
        print(result)
        return result[0]

    def total_appl_23_count():
        """
            This function gives the total count of students registered for the year 2023.
        """
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect()
        cursor.execute(" SELECT COUNT(*) FROM application_page where phd_registration_year='2023' ")
        result = cursor.fetchone()
        print(result)
        return result[0]

    def news_fetch():
        """
            This function returns the news added which are shown on homepage.
        """
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect()
        cursor.execute(" SELECT * FROM news_and_updates ORDER BY id DESC LIMIT 5 ")
        result = cursor.fetchall()
        return result

    @homepage_blueprint.route('/viewallnews', methods=['GET', 'POST'])
    def viewallnews():
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute(" SELECT * FROM news_and_updates ")
        result = cursor.fetchall()
        return render_template('Homepage/viewallnews.html', result=result)

    # ----------- END HOMEPAGE ------------------

    # ---------------------------------
    #           ABOUT US
    # ---------------------------------
    @homepage_blueprint.route('/aboutus')
    def aboutus():
        """
        This function is for the About us Page on the Homepage.
        """
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'
        return render_template('Homepage/aboutus.html', language=language, multilingual_content=multilingual_content)

    # ----------- END ABOUT US ------------------

    # ---------------------------------
    #           GR PAGE
    # ---------------------------------
    @homepage_blueprint.route('/gr_page')
    def gr_page():
        """
            This function is for the Government Resolution Page on the Homepage.
        """
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'
        return render_template('Homepage/gr_page.html', language=language, multilingual_content=multilingual_content)

    # ----------- END GR PAGE ------------------

    # ---------------------------------
    #           CONTACT US
    # ---------------------------------
    @homepage_blueprint.route('/contact')
    def contact_us():  # --------------------------  CONTACT US PAGE
        """
            This function is for the Contact us page on Homepage and it renders the map using Folium.
        """
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'
        # Create a folium map centered at Pune, India
        m = folium.Map(location=[18.5204, 73.8567], zoom_start=12)
        # Add a marker at Pune, India
        folium.Marker(location=[18.5204, 73.8567], popup="Pune, India").add_to(m)
        # Render the map in the template
        map_html = m._repr_html_()
        # Pass the map HTML to the template
        return render_template('Homepage/contact.html', map=map_html, language=language,
                               multilingual_content=multilingual_content)

    # Submit Form on Contact Us Page
    @homepage_blueprint.route('/contact_submit', methods=['GET', 'POST'])
    def contact_submit():
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect()
        if request.method == 'POST':
            ticket = 'Contact Us'
            fullname = request.form['fullname']
            email = request.form['email']
            issue_subject = request.form['issue_subject']
            description = request.form['description']

            sql = "INSERT INTO issue_raised (ticket, fullname, email, issue_subject, description) " \
                  "VALUES (%s, %s, %s, %s, %s)"
            # Execute the SQL statement with the data
            cursor.execute(sql, (ticket, fullname, email, issue_subject, description))
            cnx.commit()
            cursor.close()
            cnx.close()
            return render_template('Homepage/contact.html', language=language,
                                   multilingual_content=multilingual_content)
        return redirect(url_for('homepage.contact_us'))

    # ---------------------------------
    #           END CONTACT US
    # ---------------------------------

    # ---------------------------------
    #           REPORTS PAGE
    # ---------------------------------
    @homepage_blueprint.route('/charts')
    def reports():
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'
        # twentyone_count = year_twentyone_count()
        # twentytwo_count = year_twentytwo_count()
        # twentythree_count = year_twentythree_count()
        # male_count = male_count_report()
        # female_count = female_count_report()
        # trans_count = trans_count_report()
        # disability_yes = disability_yes_count_report()
        # disability_no = disability_no_count_report()
        return render_template('Homepage/report_homepage.html',
                               multilingual_content=multilingual_content, language=language)

    # ---------------------------------
    #           END REPORTS PAGE
    # ---------------------------------

    # ---------------------------------
    #           FAQ PAGE
    # ---------------------------------
    @homepage_blueprint.route('/faq')
    def faq():
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'
        return render_template('Homepage/FAQ.html', multilingual_content=multilingual_content, language=language)
    # ---------------------------------
    #           END FAQ PAGE
    # ---------------------------------