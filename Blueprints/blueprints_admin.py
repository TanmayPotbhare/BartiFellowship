# Login Blueprint
from PythonFiles.AdminPages.adminlogin import adminlogin_blueprint, adminlogin_auth
from PythonFiles.AdminPages.Dashboard.admin_dashboard import admin_dashboard_blueprint, admin_dashboard_auth
from PythonFiles.AdminPages.myprofile_admin import myprofile_admin_blueprint, myprofile_admin_auth

# Dashboard Sidebar Routes Blueprints
from PythonFiles.AdminPages.AdminLevels.admin_level_one import adminlevelone_blueprint, adminlevelone_auth
from PythonFiles.AdminPages.AdminLevels.admin_level_two import adminleveltwo_blueprint, adminleveltwo_auth
from PythonFiles.AdminPages.AdminLevels.admin_level_three import adminlevelthree_blueprint, adminlevelthree_auth
from PythonFiles.AdminPages.PaymentSheet.payment_sheet import payment_sheet_blueprint, payment_sheet_auth
from PythonFiles.AdminPages.PaymentSheet.payment_approval import payment_approval_blueprint, payment_approval_auth
from PythonFiles.AdminPages.PaymentSheet.fellowship_details import fellowshipdetails_blueprint, fellowshipdetails_auth
from PythonFiles.AdminPages.payment_tracking import payment_tracking_blueprint, payment_tracking_auth
from PythonFiles.AdminPages.document_repo import document_repo_blueprint, document_repo_auth
from PythonFiles.AdminPages.fellowship_awarded import fellowship_awarded_blueprint, fellowship_awarded_auth
from PythonFiles.AdminPages.withdraw_applications import withdraw_application_blueprint, withdraw_application_auth
from PythonFiles.AdminPages.sendbulkemails import bulkemails_blueprint, bulkemails_auth
from PythonFiles.AdminPages.student_management import managestudents_blueprint, managestudents_auth
from PythonFiles.AdminPages.issue_raised import issue_raised_blueprint, issue_raised_auth
from PythonFiles.AdminPages.news import news_blueprint, news_auth

# Export to Excel Python Blueprints
from PythonFiles.AdminPages.ExportExcel.adminlevels_One import adminlevels_blueprint, adminlevels_auth
from PythonFiles.AdminPages.ExportExcel.adminlevels_Two import adminlevels_Two_blueprint, adminlevels_Two_auth
from PythonFiles.AdminPages.ExportExcel.adminlevels_Three import adminlevels_Three_blueprint, adminlevels_Three_auth


# Function to register admin blueprints
def admin_blueprints(app, mail):
    # Admin Login
    adminlogin_auth(app)
    app.register_blueprint(adminlogin_blueprint)

    # Admin Dashboard Page
    admin_dashboard_auth(app)
    app.register_blueprint(admin_dashboard_blueprint)

    # Admin My Profile Page
    myprofile_admin_auth(app)
    app.register_blueprint(myprofile_admin_blueprint)

    # Admin Level One
    adminlevelone_auth(app, mail)
    app.register_blueprint(adminlevelone_blueprint)

    # Admin Level One
    adminleveltwo_auth(app, mail)
    app.register_blueprint(adminleveltwo_blueprint)

    # Admin Level Three
    adminlevelthree_auth(app, mail)
    app.register_blueprint(adminlevelthree_blueprint)

    # Payment Sheet
    payment_sheet_auth(app)
    app.register_blueprint(payment_sheet_blueprint)

    # Payment Approval
    payment_approval_auth(app)
    app.register_blueprint(payment_approval_blueprint)

    # Fellowship Details
    fellowshipdetails_auth(app)
    app.register_blueprint(fellowshipdetails_blueprint)

    # Payment Tracking Page
    payment_tracking_auth(app)
    app.register_blueprint(payment_tracking_blueprint)

    # Document Repo Page
    document_repo_auth(app)
    app.register_blueprint(document_repo_blueprint)

    # Fellowship Awarded Page
    fellowship_awarded_auth(app)
    app.register_blueprint(fellowship_awarded_blueprint)

    # Withdraw Applications
    withdraw_application_auth(app)
    app.register_blueprint(withdraw_application_blueprint)

    # Bulk Emails
    bulkemails_auth(app, mail)
    app.register_blueprint(bulkemails_blueprint)

    # Student Management Dashboard
    managestudents_auth(app)
    app.register_blueprint(managestudents_blueprint)

    # Issue Raised Page
    issue_raised_auth(app)
    app.register_blueprint(issue_raised_blueprint)

    # News Page
    news_auth(app)
    app.register_blueprint(news_blueprint)

    # ------------------------------------------------------
    # ------- The Export to Excel Blueprints ---------------

    # Admin Levels (Level 1, 2, 3)
    adminlevels_auth(app)
    app.register_blueprint(adminlevels_blueprint)

    # Admin Levels (Level 1, 2, 3)
    adminlevels_Two_auth(app)
    app.register_blueprint(adminlevels_Two_blueprint)

    # Admin Levels (Level 1, 2, 3)
    adminlevels_Three_auth(app)
    app.register_blueprint(adminlevels_Three_blueprint)