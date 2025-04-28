from PythonFiles.CandidatePages.candidate_dashboard import candidate_dashboard_blueprint, candidate_dashboard_auth
from PythonFiles.CandidatePages.manage_profile import manage_profile_blueprint, manage_profile_auth
from PythonFiles.CandidatePages.raise_issue import raise_issue_blueprint, raise_issue_auth

from PythonFiles.CandidatePages.ApplicationForm.section1 import section1_blueprint, section1_auth
from PythonFiles.CandidatePages.ApplicationForm.section2 import section2_blueprint, section2_auth
from PythonFiles.CandidatePages.ApplicationForm.section3 import section3_blueprint, section3_auth
from PythonFiles.CandidatePages.ApplicationForm.section4 import section4_blueprint, section4_auth
from PythonFiles.CandidatePages.ApplicationForm.section5 import section5_blueprint, section5_auth
from PythonFiles.CandidatePages.ApplicationForm.application_form_pdf import app_pdf_blueprint, app_pdf_auth

from PythonFiles.CandidatePages.joining_report import joining_report_blueprint, joining_report_auth
from PythonFiles.CandidatePages.installments import installments_blueprint, installments_auth
from PythonFiles.CandidatePages.presenty_report import presenty_blueprint, presenty_auth
from PythonFiles.CandidatePages.award_letter import award_letter_blueprint, award_letter_auth
from PythonFiles.CandidatePages.halfyearly import halfyearly_blueprint, halfyearly_auth
from PythonFiles.CandidatePages.hra_report import hra_report_blueprint, hra_report_auth
from PythonFiles.CandidatePages.undertaking_report import undertaking_report_blueprint, undertaking_report_auth
from PythonFiles.CandidatePages.continuation_report import continuation_report_blueprint, continuation_report_auth
from PythonFiles.CandidatePages.srf_report import srf_report_blueprint, srf_report_auth
from PythonFiles.CandidatePages.utilization_report import utilization_report_blueprint, utilization_report_auth
from PythonFiles.CandidatePages.affidavit import affidavit_report_blueprint, affidavit_auth
from PythonFiles.CandidatePages.withdraw_fellowship import withdraw_fellowship_blueprint, withdraw_fellowship_auth
from PythonFiles.CandidatePages.change_guide import change_guide_blueprint, change_guide_auth
from PythonFiles.CandidatePages.change_center import change_center_blueprint, change_center_auth
from PythonFiles.CandidatePages.upload_phd import upload_phd_blueprint, upload_phd_auth
from PythonFiles.CandidatePages.upload_thesis import upload_thesis_blueprint, upload_thesis_auth
from PythonFiles.CandidatePages.document_paths import documentpaths_blueprint, documentpaths_auth
from PythonFiles.CandidatePages.feedback import feedback_blueprint, feedback_auth


# Function to register homepage blueprints
def candidate_blueprints(app, mail):
    # Candidate Dashboard Page
    candidate_dashboard_auth(app)
    app.register_blueprint(candidate_dashboard_blueprint)

    # Candidate Dashboard Manage ProfilePage
    manage_profile_auth(app)
    app.register_blueprint(manage_profile_blueprint)
    
    # Candidate Dashboard - Raise Issue Page
    raise_issue_auth(app)
    app.register_blueprint(raise_issue_blueprint)


    # Section1 Application form
    section1_auth(app)
    app.register_blueprint(section1_blueprint)

    # Section2 Application form
    section2_auth(app)
    app.register_blueprint(section2_blueprint)

    # Section3 Application form
    section3_auth(app)
    app.register_blueprint(section3_blueprint)

    # Section4 Application form
    section4_auth(app)
    app.register_blueprint(section4_blueprint)

    # Section4 Application form
    section5_auth(app)
    app.register_blueprint(section5_blueprint)

    # Section4 Application form
    app_pdf_auth(app)
    app.register_blueprint(app_pdf_blueprint)

    # Document Paths form
    documentpaths_auth(app)
    app.register_blueprint(documentpaths_blueprint)

    # Candidate Joining Report
    joining_report_auth(app)
    app.register_blueprint(joining_report_blueprint)

    # Candidate Presenty Report
    presenty_auth(app)
    app.register_blueprint(presenty_blueprint)

    # Candidate Half Yearly Report
    halfyearly_auth(app)
    app.register_blueprint(halfyearly_blueprint)

    # Candidate Half Yearly Report
    hra_report_auth(app)
    app.register_blueprint(hra_report_blueprint)

    # Candidate Award Letter
    award_letter_auth(app)
    app.register_blueprint(award_letter_blueprint)

    # Candidate Installments
    installments_auth(app)
    app.register_blueprint(installments_blueprint)

    # Candidate Undertaking Report
    undertaking_report_auth(app)
    app.register_blueprint(undertaking_report_blueprint)

    # Candidate continuation Report
    continuation_report_auth(app)
    app.register_blueprint(continuation_report_blueprint)

    # Candidate SRF Reports
    srf_report_auth(app)
    app.register_blueprint(srf_report_blueprint)

    # Candidate Assessment Report
    utilization_report_auth(app)
    app.register_blueprint(utilization_report_blueprint)

    # Candidate Assessment Report
    affidavit_auth(app)
    app.register_blueprint(affidavit_report_blueprint)

    # Candidate Withdraw Fellowship
    withdraw_fellowship_auth(app)
    app.register_blueprint(withdraw_fellowship_blueprint)

    # Candidate Change Guide Fellowship
    change_guide_auth(app)
    app.register_blueprint(change_guide_blueprint)

    # Candidate Change Center Fellowship
    change_center_auth(app)
    app.register_blueprint(change_center_blueprint)

    # Candidate Upload Ph.D. Fellowship
    upload_phd_auth(app)
    app.register_blueprint(upload_phd_blueprint)

    # Candidate Upload Thesis Fellowship
    upload_thesis_auth(app)
    app.register_blueprint(upload_thesis_blueprint)

    # Candidate Upload Thesis Fellowship
    feedback_auth(app)
    app.register_blueprint(feedback_blueprint)



