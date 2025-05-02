import mysql.connector

# All the hosts to load on the respective servers.# All the hosts to load on the respective servers.
class HostConfig:
    hostserver = '192.168.10.69'
    # preserver = '192.168.10.69:85'
    localserver = '127.0.0.1'
    host = hostserver


class ConnectParam:
    def __init__(self, host):
        self.host = host

    def connect(self, use_dict=False):
        cnx = mysql.connector.connect(
            user='root1',
            password='Admin@#$123',
            host=self.host,
            database='BartiApplication'
        )
        cursor = cnx.cursor(dictionary=use_dict)
        return cnx, cursor


class ConfigPaths:
    paths = {
        HostConfig.localserver: {
            'USER_DOC_SEC_FIVE': 'static/uploads/user_doc_secfive/',
            'RENT_AGREEMENT_REPORT': 'static/uploads/rent_agreement/',
            'HALF_YEARLY_REPORTS': 'static/uploads/half_yearly/',
            'PRESENTY_REPORTS': 'static/uploads/presenty_reports/',
            'UPLOAD_PHOTO_SECTION1': 'static/uploads/image_retrive/',
            'PDF_STORAGE_PATH': 'static/pdf_application_form/pdfform.pdf',
            'AWARD_LETTER': 'static/pdf_application_form/award_letter.pdf',
            'JOINING_REPORT': 'static/uploads/joining_reports/',
            'PDF_CERTIFICATE': 'static/uploads/phd_certificate/',
            'UPLOAD_THESIS': 'static/uploads/upload_thesis/',
            'EMAIL_DOCS': 'static/uploads/sendbulkemails/',
            'HRA_UTILITY_REPORT': 'static/uploads/hra_utility_report/',
            'FELLOWSHIP_UTILITY_REPORT': 'static/uploads/fellowship_utility_report/',
            'UNDERTAKING_REPORT': 'static/uploads/undertaking_doc/',
            'CONTINUATION_REPORT': 'static/uploads/continuation_doc/',
            'UPGRADATION_REPORT': 'static/uploads/upgradation_doc/',
            'THREE_MEMBER_COMMITTEE_REPORT': 'static/uploads/three_member_committee_doc/',
            'AFFIDAVIT_REPORT': 'static/uploads/affidavit_report/',
            'RESEARCH_PAPER_FEEDBACK': 'static/uploads/research_paper_feedback/',
            'SAVE_NEWS': 'static/uploads/save_news/',
            # Add other paths here

            # ------ For PDF paths which is on this path: PythonFiles/CandidatePages/ApplicationForm/application_form_pdf.py
            'barti_image': 'static/assets/img/logo/barti_new.png',
            'diya_image': 'static/assets/img/logo/diya.png',
            'dr_ambedkar_image': 'static/admin_assets/images/b-r-ambedkar.png',
            'absolute_path': ''
        },
        HostConfig.hostserver: {
            'USER_DOC_SEC_FIVE': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/uploads/user_doc_secfive/',
            'RENT_AGREEMENT_REPORT': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/uploads/rent_agreement/',
            'HALF_YEARLY_REPORTS': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/uploads/half_yearly/',
            'PRESENTY_REPORTS': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/uploads/presenty_reports/',
            'UPLOAD_PHOTO_SECTION1': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/uploads/image_retrive/',
            'PDF_STORAGE_PATH': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/pdf_application_form/pdfform.pdf',
            'AWARD_LETTER': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/pdf_application_form/award_letter.pdf',
            'JOINING_REPORT': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/uploads/joining_reports/',
            'PDF_CERTIFICATE': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/uploads/phd_certificate/',
            'UPLOAD_THESIS': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/uploads/upload_thesis/',
            'EMAIL_DOCS': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/uploads/sendbulkemails/',
            'HRA_UTILITY_REPORT': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/uploads/hra_utility_report/',
            'FELLOWSHIP_UTILITY_REPORT': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/uploads/fellowship_utility_report/',
            'UNDERTAKING_REPORT': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/uploads/undertaking_doc/',
            'CONTINUATION_REPORT': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/uploads/continuation_doc/',
            'THREE_MEMBER_COMMITTEE_REPORT': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/uploads/three_member_committee_doc/',
            'UPGRADATION_REPORT': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/uploads/upgradation_doc/',
            'AFFIDAVIT_REPORT': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/uploads/affidavit_report/',
            'RESEARCH_PAPER_FEEDBACK': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/uploads/research_paper_feedback/',
            'SAVE_NEWS': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/uploads/save_news/',
            # Add other paths here


            # ------ For PDF paths which is on this path: PythonFiles/CandidatePages/ApplicationForm/application_form_pdf.py
            'barti_image': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/assets/img/logo/barti_new.png',
            'diya_image': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/assets/img/logo/diya.png',
            'dr_ambedkar_image': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/admin_assets/images/b-r-ambedkar.png',
            'absolute_path': '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship'
        }
    }


class MySQLDatabase:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.connection.commit()
        return cursor

    def fetch_all(self, cursor):
        return cursor.fetchall()

    def fetch_one(self, cursor):
        return cursor.fetchone()
