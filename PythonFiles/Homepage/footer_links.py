from classes.database import HostConfig, ConfigPaths
from flask import Blueprint, render_template, session, request, jsonify
from PythonFiles.Homepage.multilingual_content import multilingual_content

footer_links_blueprint = Blueprint('footer_links', __name__)


def footer_links_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    # --------------------------------------------------------------------
    # -------------      FOOTER FUNCTIONALITY     -----------
    # --------------------------------------------------------------------
    @footer_links_blueprint.route('/hyperlink_policy')
    def hyperlink_policy():
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'
        return render_template('Homepage/FooterLinks/hyperlink_policy.html', multilingual_content=multilingual_content,
                               language=language)

    @footer_links_blueprint.route('/t_and_c')
    def t_and_c():
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'
        return render_template('Homepage/FooterLinks/t_and_c.html', multilingual_content=multilingual_content,
                               language=language)

    @footer_links_blueprint.route('/privacy_policy')
    def privacy_policy():
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'
        return render_template('Homepage/FooterLinks/privacy_policy.html', multilingual_content=multilingual_content,
                               language=language)

    @footer_links_blueprint.route('/copyright_policy')
    def copyright_policy():
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'
        return render_template('Homepage/FooterLinks/copyright_policy.html', multilingual_content=multilingual_content,
                               language=language)

    @footer_links_blueprint.route('/wmp_policy')
    def wmp_policy():
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'
        return render_template('Homepage/FooterLinks/wmp_policy.html', multilingual_content=multilingual_content,
                               language=language)

    @footer_links_blueprint.route('/sitemap')
    def sitemap():
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'
        return render_template('Homepage/FooterLinks/sitemap.html', multilingual_content=multilingual_content,
                               language=language)

    @footer_links_blueprint.route('/update_preview_form', methods=['POST'])
    def update_preview_form():
        if request.method == 'POST':
            data = request.form.to_dict(flat=False)
            return jsonify(request.form)
