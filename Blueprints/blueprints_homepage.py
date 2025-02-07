# blueprints_homepage.py

from PythonFiles.Homepage.homepage import homepage_blueprint, homepage_auth
from PythonFiles.Homepage.login_signup import login_blueprint, login_auth
from PythonFiles.Homepage.footer_links import footer_links_blueprint, footer_links_auth


# Function to register homepage blueprints
def homepage_blueprints(app, mail):
    # Homepage
    homepage_auth(app)
    app.register_blueprint(homepage_blueprint)

    # Login/Signup
    login_auth(app, mail)
    app.register_blueprint(login_blueprint)

    # Footer Links
    footer_links_auth(app)
    app.register_blueprint(footer_links_blueprint)
