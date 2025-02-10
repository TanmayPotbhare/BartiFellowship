from datetime import date, timedelta, datetime
import mysql.connector
from classes.database import HostConfig, ConfigPaths, ConnectParam
import os
from flask_mail import Mail, Message
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from Authentication.middleware import auth

news_blueprint = Blueprint('news', __name__)


def news_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @news_blueprint.route('/news', methods=['GET', 'POST'])
    def news():
        host = HostConfig.host
        connect_param = ConnectParam(host)

        # Select all records after the insertion
        cnx, cursor = connect_param.connect(use_dict=True)
        cursor.execute("SELECT * FROM news_and_updates")
        result = cursor.fetchall()
        # print('result', result)
        # Close the cursor and connection
        cursor.close()
        cnx.close()
        return render_template('AdminPages/news.html', result=result)

    @news_blueprint.route('/news_submit', methods=['GET', 'POST'])
    def news_submit():
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        if request.method == 'POST':
            user = request.form['user']
            title = request.form['title']
            subtitle = request.form['subtitle']
            date = datetime.now()
            time = date.strftime('%H:%M:%S')
            doc = save_news(request.files['doc'])
            sql = """ INSERT INTO news_and_updates(user, title, subtitle, date, time, doc) VALUES(%s, %s, %s, %s, %s, %s) """
            data = (user, title, subtitle, date, time, doc)

            # Create cursor
            cnx, cursor = connect_param.connect(use_dict=True)
            cursor.execute(sql, data)
            # Commit the changes
            cnx.commit()
            cursor.close()
            flash('News has been added successfully', 'success')
            return redirect(url_for('news.news'))
        return redirect(url_for('news.news'))

    def save_news(file):
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['SAVE_NEWS'], filename))
            # return os.path.join(app.config['RENT_AGREEMENT_REPORT'], filename)
            return '/static/uploads/save_news/' + filename
        else:
            return "Save File"