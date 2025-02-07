import tempfile
from datetime import datetime
import requests
import os
from fpdf import FPDF
from classes.caste import casteController
from classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response, jsonify, \
    Response

app_pdf_blueprint = Blueprint('app_pdf', __name__)


def app_pdf_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @app_pdf_blueprint.route('/generate_pdf', methods=['GET', 'POST'])
    def generate_pdf():
        email = session['email']
        output_filename = app.config['PDF_STORAGE_PATH']
        # output_filename = 'static/pdf_application_form/pdfform.pdf'

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute(" SELECT * FROM signup WHERE year IN ('2020', '2021', '2022') and email = %s ", (email,))
        output = cursor.fetchall()

        if output:
            cursor.execute(
                "SELECT * FROM application_page WHERE email = %s", (email,))
            old_user_data = cursor.fetchone()
            # print(old_user_data)
            # Generate a styled PDF
            # print(output_filename)
            generate_pdf_with_styling(old_user_data, output_filename)
        else:
            cursor.execute("SELECT * FROM application_page WHERE email = %s", (email,))
            data = cursor.fetchone()
            # print(data)
            # Generate a styled PDF
            generate_pdf_with_styling(data, output_filename)

        # Serve the generated PDF as a response
        with open(output_filename, "rb") as pdf_file:
            response = Response(pdf_file.read(), content_type="application/pdf")
            response.headers['Content-Disposition'] = 'inline; filename=Application Form.pdf'

        return response

    def generate_pdf_with_styling(data, filename):
        class PDF(FPDF):
            header_added = False  # To track whether the header is added to the first page

            def header(self):
                if not self.header_added:
                    # /
                    self.set_font("Arial", "B", 12)
                    # self.cell(0, 10, "Fellowship ", align="C", ln=True)
                    # Add space by changing the second parameter (e.g., 20)
                    # Insert an image (symbol) at the center of the header

                    self.image('static/assets/img/logo/barti_new.png', 10, 10, 23)
                    # self.image('static/Images/satya.png', 175, 10, 20)
                    self.image('static/assets/img/logo/diya.png', 175, 10, 23)
                    self.image('static/admin_assets/images/b-r-ambedkar.png', 95, 10, 13)  # Center the image
                    # self.image('/var/www/fellowship/fellowship/FellowshipPreServer/static/Images/trti.jpeg', 10, 10, 20)
                    # self.image('/var/www/fellowship/fellowship/FellowshipPreServer/static/Images/satya.png', 155, 10, 20)
                    # self.image('/var/www/fellowship/fellowship/FellowshipPreServer/static/Images/maharashtra_shasn.png', 175, 10, 20)
                    self.ln(8)
                    self.set_font("Arial", size=12)  # Larger font for the main heading
                    # self.cell(0, 20)
                    self.cell(0, 20, "Dr. Babasaheb Ambedkar Research & Training Institute (BARTI), Pune ", align="C",
                              ln=True)  # Adjust vertical spacing as needed
                    current_y = self.get_y()  # Get the current y-position

                    self.set_font("Arial", size=9)
                    self.set_y(current_y)  # Reset y to the position after the main heading
                    self.cell(0, 1,
                              "(An Autonomous Institute of the Department of Social Justice and Special Assistance, Government of Maharashtra)",
                              align="C", ln=True)

                    current_y = self.get_y()

                    self.set_font("Arial", size=8)
                    self.set_y(current_y)
                    self.cell(0, 8, "Queen's Garden, 28 VVIP Circuit House, Pune, Maharashtra 411001", align="C",
                              ln=True)

                    # Remove the self.ln(4) here
                    self.line(10, self.get_y(), 200, self.get_y())  # Draw a line

                    # ----------------------------------------------------
                    # Blue Box and heading inside that.
                    self.set_font("Arial", "B", 11)
                    fellowship_year = data['fellowship_application_year']
                    pdf.set_fill_color(0, 0, 139)  # Dark blue RGB
                    # Set the text color to white
                    pdf.set_text_color(255, 255, 255)  # White color
                    # Add the text inside the box
                    pdf.cell(0, 10,
                             f"Fellowship BANRF {int(fellowship_year)} - {int(fellowship_year) + 1}",
                             align="C", ln=True, fill=True)
                    # ------------------- Blue Box -----------------------
                    self.ln(2)  # Adjust this value to control the space after the line

                    # ----------------------------------------------------
                    # Image Alignment and Call
                    self.ln(1)
                    image_x = 173  # Adjust this to place the image further to the right if needed
                    image_y = self.get_y()  # Current y-position of the cursor after the blue box
                    # Insert the image to the right
                    # photo = '/var/www/fellowship/fellowship/FellowshipPreServer' + data['applicant_photo']
                    photo = data['applicant_photo']
                    modified_path = photo[1:] if photo.startswith("/") else photo
                    # Define image size (width, height)
                    image_width = 25
                    image_height = 25
                    # Draw a rectangle border around the image
                    border_padding = 2  # Padding around the image within the border
                    self.set_draw_color(0, 0, 0)  # Set border color to black
                    self.rect(image_x - border_padding, image_y - border_padding, image_width + 2 * border_padding,
                              image_height + 2 * border_padding)  # Draw border around the image
                    # Insert the image inside the border
                    self.image(modified_path, image_x, image_y, image_width, image_height)
                    # ----------------- END Image --------------------------------

                    # ----------------------------------------------------
                    # Key-Value Fields on the Left
                    self.set_font("Arial", size=10)
                    self.set_text_color(0, 0, 0)  # Black color

                    # Set the left margin to ensure proper alignment
                    left_margin = 10  # Margin for left alignment
                    key_width = 50  # Fixed width for keys
                    value_width = 50  # Remaining width for values (adjust as needed)

                    key_value_spacing = 5  # Space between key-value pairs

                    # Define the key-value pairs
                    key_value_pairs = [
                        ("Applicant ID:", f"BARTI/BANRF{data.get('phd_registration_year', 'XXXX')}/{data.get('id', 'XXXX')}"),
                        ("Full Name:",
                         f"{data.get('first_name', '')} {data.get('middle_name', '')} {data.get('last_name', '')}"),
                        ("Submitted Date:", str(data.get('application_date', 'N/A'))),
                        ("Submitted Time:", str(data.get('application_time', 'N/A')))
                    ]

                    # Add space before key-value fields
                    self.ln(5)  # Adds a line break, adjust this value if needed

                    # Iterate through the key-value pairs and display them
                    for key, value in key_value_pairs:
                        # Print the key (with fixed width for alignment)
                        self.set_x(left_margin)  # Set x position to ensure left alignment
                        self.cell(key_width, key_value_spacing, key, align="L", ln=False)  # Print the key
                        # Print the value (with remaining width)
                        self.cell(value_width, key_value_spacing, value, align="L", ln=True)  # Print the value

                    # Adjust line break if you need more space after the key-value fields
                    self.ln(5)
                    self.ln(5)

                    self.header_added = True  # Set to True after adding the header

            def footer(self):
                # Add a footer
                self.set_y(-15)
                self.set_font("Arial", "B", 8)
                self.cell(0, 10, f" {self.page_no()} ", align="L")
                fellowship_year = data['fellowship_application_year']
                # Center-align the "TRTI" text
                self.cell(0, 10, f" BARTI  |  Fellowship | {int(fellowship_year)} - {int(fellowship_year) + 1}", align="R")

                self.set_draw_color(0, 0, 0)  # Border color (black)
                padding = 7
                self.rect(padding, padding, 210 - 2 * padding, 297 - 2 * padding)  # Draw border on each page


        personal_details = {
            "Adhaar Number:": data['adhaar_number'],
            "First Name:": data['first_name'],
            "Middle Name:": data['middle_name'],
            "Last Name:": data['last_name'],
            "Mobile Number:": data['mobile_number'],
            "Email:": data['email'],
            "Date of Birth:": data['date_of_birth'],
            "Gender:": data['gender'],
            "Age:": data['age'],
            "Category:": 'Scheduled Caste',
            "Caste: ": data['your_caste']

            # Add more fields as needed
        }

        address_details = {
            "Permanent Address:": data['add_1'],
            "Pincode:": data['pincode'],
            "Village:": data['village'],
            "Taluka:": data['taluka'],
            "District:": data['district'],
            "State:": data['state']
        }

        com_address_details = {
            "Communication Address:": data['comm_add_1'],
            "Comm. Pincode:": data['comm_pincode'],
            "Comm. Village:": data['comm_village'],
            "Comm. Taluka:": data['comm_taluka'],
            "Comm. District:": data['comm_district'],
            "Comm. State:": data['comm_state']
        }

        # qualification_details = {
        # SSC
        ssc = {
            "SSC Passing Year:": data['ssc_passing_year'],
            "SSC School Name:": data['ssc_school_name'],
            "SSC Stream:": data['ssc_stream'],
            "SSC Attempts:": data['ssc_attempts'],
            "SSC Total Marks:": data['ssc_total'],
            "SSC Percentage:": data['ssc_percentage']
        }

        hsc = {
            "HSC Passing Year:": data['hsc_passing_year'],
            "HSC School Name:": data['hsc_school_name'],
            "HSC Stream:": data['hsc_stream'],
            "HSC Attempts:": data['hsc_attempts'],
            "HSC Total Marks:": data['hsc_total'],
            "HSC Percentage:": data['hsc_percentage']
        }

        grad = {
            "Graduation Passing Year:": data['graduation_passing_year'],
            "Graduation College Name:": data['graduation_school_name'],
            "Graduation Stream:": data['grad_stream'],
            "Graduation Attempts:": data['grad_attempts'],
            "Graduation Total Marks:": data['grad_total'],
            "Graduation Percentage:": data['graduation_percentage']
        }

        postgrad = {
            "Post Grad. Passing Year:": data['phd_passing_year'],
            "Post Grad. College Name:": data['phd_school_name'],
            "Post Grad. Stream:": data['pg_stream'],
            "Post Grad. Attempts:": data['pg_attempts'],
            "Post Grad. Total Marks:": data['pg_total'],
            "Post Grad. Percentage:": data['phd_percentage'],
            "Competitve Exam given:": data['have_you_qualified']
            # Add more fields as needed
        }
        if 'have_you_qualified' in data:  # Check if the key exists
            exams = data['have_you_qualified'].split(',')  # Split the string into a list
            cleaned_exams = [exam.strip() for exam in exams]  # remove extra spaces
            if "OTHER" in cleaned_exams and 'have_you_qualified_other' in data and data[
                'have_you_qualified_other'] != "":
                postgrad["Other Competitive Exam:"] = data['have_you_qualified_other']
            elif "OTHER" in cleaned_exams:
                postgrad["Other Competitive Exam:"] = "Not Specified"

        phd_details = {
            "P.H.D Registration Date:": data['phd_registration_date'],
            "P.H.D Registration Year:": data['phd_registration_year'],
            "Age at Ph.D. Registration:": data['phd_registration_age'],
            "Fellowship Application Year:": data['fellowship_application_year'],
            "Department Name:": data['department_name'],
            "Topic of Ph.D.:": data['topic_of_phd'],
            "Name of Guide:": data['name_of_guide'],
            "Faculty/Stream:": data['faculty']
        }

        # Check if 'other_college_name' key exists in data before accessing
        if 'other_university' in data and data['concerned_university'] == 'Other':
            phd_details["University Name:"] = data['other_university']
        else:
            phd_details["University Name:"] = data['concerned_university']

        # Check if 'other_college_name' key exists in data before accessing
        if 'other_college_name' in data and data['name_of_college'] == 'Other':
            phd_details["Name of College:"] = data['other_college_name']
        else:
            phd_details["Name of College:"] = data['name_of_college']


        income_details = {
            "Family Annual Income": data['family_annual_income'],
            "Income Certificate Number": data['income_certificate_number'],
            "Income Certificate Issuing Authority": data['issuing_authority'],
            "Income Certificate Issuing District": data['income_issuing_district'],
            "Income Certificate Issuing Taluka": data['income_issuing_taluka']
        }

        caste = {
            "Are you Domicile of Maharashtra": data['domicile'],
            "Domicile Certificate": data['domicile_certificate'],
            "Domicile Certificate Number": data['domicile_number'],
            "Do you have Caste/Tribe Certificate": data['caste_certf'],
            "Caste | Tribe": data['your_caste'],
            "Sub Caste/Tribe": data['subcaste'],
            "Caste Certificate Number": data['caste_certf_number'],
            "Caste Certificate Issuing District": data['issuing_district'],
            "Caste Certificate Issuing Authority": data['caste_issuing_authority'],
            "Validity Certificate": data['validity_certificate'],
            "Validity Certificate Number": data['validity_cert_number'],
            "Validity Certificate Issuing District": data['validity_issuing_district'],
            "Validity Certificate Issuing Taluka": data['validity_issuing_taluka'],
            "Validity Certificate Issuing Authority": data['validity_issuing_authority']
        }

        parent_details = {
            "Salaried": data['salaried'],
            "Disability": data['disability'],
            "Type of Disability": data['type_of_disability'],
            "Father Name": data['father_name'],
            "Mother Name": data['mother_name'],
            "Anyone Work in Government": data['work_in_government'],
            "IFSC Code": data['ifsc_code'],
            "Account Number": data['account_number'],
            "Bank Name": data['bank_name'],
            "Account Holder Name": data['account_holder_name'],
            "MICR Code": data['micr']
        }

        signature_doc = bool(data['signature'])
        adhaar_doc = bool(data['adhaar_card_doc'])
        pan_doc = bool(data['pan_card_doc'])
        domicile_doc = bool(data['domicile_doc'])
        caste_doc = bool(data['caste_doc'])
        validity_doc = bool(data['validity_doc'])
        income_doc = bool(data['income_doc'])
        ssc_doc = bool(data['ssc_doc'])
        hsc_doc = bool(data['hsc_doc'])
        grad_doc = bool(data['grad_doc'])
        postgrad_doc = bool(data['post_grad_doc'])
        entrance_doc = bool(data['entrance_doc'])
        phd_reciept_doc = bool(data['phd_reciept_doc'])
        guideAllotment_doc = bool(data['guideAllotment_doc'])
        guideAccept_doc = bool(data['guideAccept_doc'])
        rac_doc = bool(data['rac_doc'])
        confirmation_doc = bool(data['confirmation_doc'])
        joining_doc = bool(data['joining_doc'])
        annexureAC_doc = bool(data['annexureAC_doc'])
        annexureB_doc = bool(data['annexureB_doc'])
        annexureD_doc = bool(data['annexureD_doc'])
        disable_doc = bool(data['disable_doc'])
        gazete_doc = bool(data['gazete_doc'])
        selfWritten_doc = bool(data['selfWritten_doc'])
        research_letter_doc = bool(data['research_letter_doc'])

        doc_uploaded = {
            "Signature": signature_doc,
            "Adhaar Card": adhaar_doc,
            "Pan Card": pan_doc,
            "Domicile Certificate": domicile_doc,
            "Caste Certificate": caste_doc,
            "Validity Certificate": validity_doc,
            "Income Certificate": income_doc,
            "Secondary School Certificate": ssc_doc,
            "Higher Secondary Certificate": hsc_doc,
            "Graduation Certificate": grad_doc,
            "Post Graduation Certificate": postgrad_doc,
            "SET/GATE/CET Marksheet & Passing Certificate": entrance_doc,
            "Ph.D Admission Reciept": phd_reciept_doc,
            "Guide Allotment Letter": guideAllotment_doc,
            "Guide Acceptance Letter": guideAccept_doc,
            "Letter of Accpetance from RAC/RRC": rac_doc,
            "Confirmation Letter": confirmation_doc,
            "Research Center Joining Report": joining_doc,
            "Annexure A (on INR 100 Stamp Paper) & Annexure C": annexureAC_doc,
            "Guide & H.O.D Research Common letter (Annexure B)": annexureB_doc,
            "Annexure D": annexureD_doc,
            "Disability Certificate": disable_doc,
            "Change in Name - Gazzette": gazete_doc,
            "Self Written Certificate of not getting scholarship from anywhere": selfWritten_doc,
            "Research Synopsis/ Research Center Allotment letter": research_letter_doc,
        }

        pdf = PDF(orientation='P', format='A4')
        pdf.add_page()
        pdf.header()
        # pdf.image_and_date(data)

        #---------------------- Section 1 - Personal Details ----------------
        if pdf.get_y() > 270:  # Prevent overflow
            pdf.add_page()
        pdf.set_fill_color(0, 0, 139)  # Dark blue RGB
        # Set the text color to white
        pdf.set_text_color(255, 255, 255)  # White color
        # Add the text inside the box
        pdf.cell(0, 10,
                 f"Personal Details",
                 align="C", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=10)
        pdf.ln(2)

        # Set the left margin to ensure proper alignment
        left_margin = 10  # Margin for left alignment
        key_width = 50  # Fixed width for keys
        value_width = 50  # Remaining width for values (adjust as needed)

        key_value_spacing = 5  # Space between key-value pairs
        for key, value in personal_details.items():
            pdf.set_x(left_margin)  # Set x position to ensure left alignment
            pdf.cell(key_width, key_value_spacing, key, align="L", ln=False)  # Print the key
            # Print the value (with remaining width)
            pdf.cell(value_width, key_value_spacing, str(value), align="L", ln=True)  # Print the value

        pdf.ln(5)
        # ----------------------- END Section 1 ------------------------

        # --------------------------------------------------------------
        # ----------- STart Section 2 Address Details ------------------
        # Personal Details
        if pdf.get_y() > 270:  # Prevent overflow
            pdf.add_page()
        pdf.set_fill_color(0, 0, 139)  # Dark blue RGB
        # Set the text color to white
        pdf.set_text_color(255, 255, 255)  # White color
        # Add the text inside the box
        pdf.cell(0, 10,
                 f"Address Details",
                 align="C", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=10)
        pdf.ln(2)

        # Set the left margin to ensure proper alignment
        left_margin = 10
        col_width = 70  # Adjust as needed
        key_width = 30
        value_width = col_width - key_width
        key_value_spacing = 1
        vertical_line_x = left_margin + col_width

        pdf.set_x(left_margin)

        col_widths =  [90, 90] # Adjust column widths as needed
        x_start = left_margin

        perm_address_data = list(address_details.items())
        comm_address_data = list(com_address_details.items())

        max_rows = max(len(perm_address_data), len(comm_address_data))

        for i in range(max_rows):
            pdf.set_x(x_start)

            # Permanent Address
            if i < len(perm_address_data):
                label, value = perm_address_data[i]
                pdf.cell(col_widths[0] / 2, 5, label, align="L")  # Keep cell height for label
                pdf.cell(col_widths[0] / 2, 5, str(value), align="L", ln=False)  # Keep cell height for value

            else:
                pdf.cell(col_widths[0] / 2, 5, "", align="L")  # Keep cell height
                pdf.cell(col_widths[0] / 2, 5, "", align="L", ln=False)

            # Communication Address
            if i < len(comm_address_data):
                label, value = comm_address_data[i]
                pdf.cell(col_widths[1] / 2, 5, label, align="L")  # Keep cell height
                pdf.cell(col_widths[1] / 2, 5, str(value), align="L", ln=True)  # New line

            else:
                pdf.cell(col_widths[1] / 2, 5, "", align="L")  # Keep cell height
                pdf.cell(col_widths[1] / 2, 5, "", align="L", ln=True)  # New line

        pdf.ln(5)
        # --------------------- END Section 2 -----------------------------------

        # ---------------------- Section 3 - Education Details ----------------
        if pdf.get_y() > 270:  # Prevent overflow
            pdf.add_page()
        pdf.set_fill_color(0, 0, 139)  # Dark blue RGB
        # Set the text color to white
        pdf.set_text_color(255, 255, 255)  # White color
        # Add the text inside the box
        pdf.cell(0, 10,
                 f"Education Details",
                 align="C", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial","B", size=10)
        pdf.ln(2)

        pdf.cell(0, 10, "S.S.C Details", ln=True)
        pdf.set_font("Arial",  size=10)
        # Set the left margin to ensure proper alignment
        left_margin = 10  # Margin for left alignment
        key_width = 50  # Fixed width for keys
        value_width = 50  # Remaining width for values (adjust as needed)

        key_value_spacing = 5  # Space between key-value pairs
        for key, value in ssc.items():
            pdf.set_x(left_margin)  # Set x position to ensure left alignment
            pdf.cell(key_width, key_value_spacing, key, align="L", ln=False)  # Print the key
            # Print the value (with remaining width)
            pdf.cell(value_width, key_value_spacing, str(value), align="L", ln=True)  # Print the value

        pdf.set_font("Arial", "B", size=10)
        pdf.cell(0, 10, "H.S.C Details", ln=True)
        pdf.set_font("Arial", size=10)
        # Set the left margin to ensure proper alignment
        left_margin = 10  # Margin for left alignment
        key_width = 50  # Fixed width for keys
        value_width = 50  # Remaining width for values (adjust as needed)

        key_value_spacing = 5  # Space between key-value pairs
        for key, value in hsc.items():
            pdf.set_x(left_margin)  # Set x position to ensure left alignment
            pdf.cell(key_width, key_value_spacing, key, align="L", ln=False)  # Print the key
            # Print the value (with remaining width)
            pdf.cell(value_width, key_value_spacing, str(value), align="L", ln=True)  # Print the value

        pdf.set_font("Arial", "B", size=10)
        pdf.cell(0, 10, "Graduation Details", ln=True)
        pdf.set_font("Arial", size=10)
        # Set the left margin to ensure proper alignment
        left_margin = 10  # Margin for left alignment
        key_width = 50  # Fixed width for keys
        value_width = 50  # Remaining width for values (adjust as needed)

        key_value_spacing = 5  # Space between key-value pairs
        for key, value in grad.items():
            pdf.set_x(left_margin)  # Set x position to ensure left alignment
            pdf.cell(key_width, key_value_spacing, key, align="L", ln=False)  # Print the key
            # Print the value (with remaining width)
            pdf.cell(value_width, key_value_spacing, str(value), align="L", ln=True)  # Print the value

        pdf.set_font("Arial", "B", size=10)
        pdf.cell(0, 10, "Post Graduation Details", ln=True)
        pdf.set_font("Arial", size=10)
        # Set the left margin to ensure proper alignment
        left_margin = 10  # Margin for left alignment
        key_width = 50  # Fixed width for keys
        value_width = 50  # Remaining width for values (adjust as needed)

        key_value_spacing = 5  # Space between key-value pairs
        for key, value in postgrad.items():
            pdf.set_x(left_margin)  # Set x position to ensure left alignment
            pdf.cell(key_width, key_value_spacing, key, align="L", ln=False)  # Print the key
            # Print the value (with remaining width)
            pdf.cell(value_width, key_value_spacing, str(value), align="L", ln=True)  # Print the value

        pdf.ln(5)
        # ----------------------- END Section 3 ------------------------

        # ---------------------- Section 4 - Income Details ----------------
        if pdf.get_y() > 270:  # Prevent overflow
            pdf.add_page()
        pdf.set_fill_color(0, 0, 139)  # Dark blue RGB
        # Set the text color to white
        pdf.set_text_color(255, 255, 255)  # White color
        # Add the text inside the box
        pdf.cell(0, 10,
                 f"Ph.D. Details",
                 align="C", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=10)
        pdf.ln(2)

        # Set the left margin to ensure proper alignment
        left_margin = 10  # Margin for left alignment
        key_width = 70  # Fixed width for keys
        value_width = 30  # Remaining width for values (adjust as needed)

        key_value_spacing = 5  # Space between key-value pairs
        for key, value in phd_details.items():
            pdf.set_x(left_margin)  # Set x for the key
            pdf.cell(key_width, key_value_spacing, key, align="L", ln=False)

            value_str = str(value) if value is not None else ""

            # Set x for the value (important for alignment!)
            pdf.set_x(left_margin + key_width)  # Start of value

            if key == "Topic of Ph.D.":  # MultiCell for wrapping only this field
                pdf.multi_cell(value_width, key_value_spacing, value_str, align="L")
            else:  # Regular cell for other fields
                pdf.cell(value_width, key_value_spacing, value_str, align="L",
                         ln=False)  # ln=False here to prevent it going to next line
                pdf.ln(key_value_spacing)  # manually go to next line

        pdf.ln(5)
        # ----------------------- END Section 4 ------------------------

        # ---------------------- Section 4 - Income Details ----------------
        if pdf.get_y() > 270:  # Prevent overflow
            pdf.add_page()
        pdf.set_fill_color(0, 0, 139)  # Dark blue RGB
        # Set the text color to white
        pdf.set_text_color(255, 255, 255)  # White color
        # Add the text inside the box
        pdf.cell(0, 10,
                 f"Income Details",
                 align="C", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=10)
        pdf.ln(2)

        # Set the left margin to ensure proper alignment
        left_margin = 10  # Margin for left alignment
        key_width = 70  # Fixed width for keys
        value_width = 30  # Remaining width for values (adjust as needed)

        key_value_spacing = 5  # Space between key-value pairs
        for key, value in income_details.items():
            pdf.set_x(left_margin)  # Set x position to ensure left alignment
            pdf.cell(key_width, key_value_spacing, key, align="L", ln=False)  # Print the key
            # Print the value (with remaining width)
            pdf.cell(value_width, key_value_spacing, str(value), align="L", ln=True)  # Print the value

        pdf.ln(5)
        # ----------------------- END Section 4 ------------------------

        # ---------------------- Section 5 - Income Details ----------------
        if pdf.get_y() > 270:  # Prevent overflow
            pdf.add_page()
        pdf.set_fill_color(0, 0, 139)  # Dark blue RGB
        # Set the text color to white
        pdf.set_text_color(255, 255, 255)  # White color
        # Add the text inside the box
        pdf.cell(0, 10,
                 f"Caste/Tribe & Validity Details",
                 align="C", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=10)
        pdf.ln(2)

        # Set the left margin to ensure proper alignment
        left_margin = 10  # Margin for left alignment
        key_width = 70  # Fixed width for keys
        value_width = 30  # Remaining width for values (adjust as needed)

        key_value_spacing = 5  # Space between key-value pairs
        for key, value in caste.items():
            pdf.set_x(left_margin)  # Set x position to ensure left alignment
            pdf.cell(key_width, key_value_spacing, key, align="L", ln=False)  # Print the key
            # Print the value (with remaining width)
            pdf.cell(value_width, key_value_spacing, str(value), align="L", ln=True)  # Print the value

        pdf.ln(5)
        # ----------------------- END Section 5 ---------------------------------

        # ---------------------- Section 6 - Bakk Details ----------------
        pdf.ln(3)
        if pdf.get_y() > 270:  # Prevent overflow
            pdf.add_page()
        pdf.set_fill_color(0, 0, 139)  # Dark blue RGB
        # Set the text color to white
        pdf.set_text_color(255, 255, 255)  # White color
        # Add the text inside the box
        pdf.cell(0, 10,
                 f"Bank & Parent Details",
                 align="C", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=10)
        pdf.ln(2)

        # Set the left margin to ensure proper alignment
        left_margin = 10  # Margin for left alignment
        key_width = 50  # Fixed width for keys
        value_width = 30  # Remaining width for values (adjust as needed)

        key_value_spacing = 5  # Space between key-value pairs
        for key, value in parent_details.items():
            pdf.set_x(left_margin)  # Set x position to ensure left alignment
            pdf.cell(key_width, key_value_spacing, key, align="L", ln=False)  # Print the key
            # Print the value (with remaining width)
            pdf.cell(value_width, key_value_spacing, str(value), align="L", ln=True)  # Print the value

        pdf.ln(5)
        # ----------------------- END Section 6 ---------------------------------

        # ---------------------- Section 7 - Docs Details ----------------
        if pdf.get_y() > 270:  # Prevent overflow
            pdf.add_page()
        pdf.set_fill_color(0, 0, 139)  # Dark blue RGB
        # Set the text color to white
        pdf.set_text_color(255, 255, 255)  # White color
        # Add the text inside the box
        pdf.cell(0, 10,
                 f"Documents Uploaded",
                 align="C", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=10)
        pdf.ln(2)

        # Set the left margin to ensure proper alignment
        left_margin = 10  # Margin for left alignment
        key_width = 50  # Fixed width for keys
        value_width = 25  # Remaining width for values (adjust as needed)

        key_value_spacing = 6  # Space between key-value pairs
        image_width = 3  # Reduced image width
        image_height = 3 # Reduced image height
        image_offset_x = 2  # Offset to fine-tune horizontal position
        image_offset_y = 1  # Offset to fine-tune vertical position

        for key, value in doc_uploaded.items():
            pdf.set_x(left_margin)
            pdf.cell(key_width, key_value_spacing, key, align="L", ln=False)

            if value:
                image_path = "static/assets/img/logo/check_mark.png"
            else:
                image_path = "static/assets/img/logo/cross_icon.png"

            try:
                pdf.image(image_path, x=pdf.get_x() + key_width + image_offset_x, y=pdf.get_y() + image_offset_y,
                          w=image_width, h=image_height)
            except Exception as e:
                print(f"Error adding image: {e}")
                pdf.set_text_color(255, 0, 0)
                pdf.cell(10, key_value_spacing, "Error", align="L", ln=False)
                pdf.set_text_color(0, 0, 0)

            pdf.cell(value_width - 10 - image_width, key_value_spacing, align="L", ln=True)  # Adjust width

        pdf.ln(5)
        # ----------------------- END Section 7 ---------------------------------

        pdf.line(10, pdf.get_y(), 200, pdf.get_y())

        pdf.ln(10)
        pdf.set_fill_color(0, 0, 139)  # Dark blue RGB
        # Set the text color to white
        pdf.set_text_color(255, 255, 255)  # White color
        # Add the text inside the box
        pdf.cell(0, 10,
                 f"Policy & Undertaking",
                 align="C", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)  # White color
        pdf.ln(2)

        # Checkboxes and Text
        checkbox_size = 4
        checkbox_spacing = 3
        page_width = 210 - 2 * left_margin

        # Checkbox and Text Section
        pdf.set_font("Arial", size=10)  # Set a suitable font size for the checkboxes
        fullname = data['first_name'] + ' ' + data['middle_name'] + ' ' + data['last_name']

        for text in [
            f"I {fullname} hereby declare by signing below that the above particulars are true and correct to the best of my knowledge and belief and nothing has been concealed therein.",
            "If in the future I am granted financial aid or a scholarship from any other university grants commission / any other government institution / any other financial aid organization / college / government, or if I secure full-time or part-time employment / job / business / self-employment, I assure that I will inform the Dr. Babasaheb Ambedkar Research and Training Institute, Pune about this and will return the entire amount of financial aid received from the Dr. Babasaheb Ambedkar Research and Training Institute, Pune.",
            "We respect your privacy and shall only collect and use as much personal information from you as is required to administer your account and provide the products and services you have requested from us. If we should require additional information from you, we shall collect and use the same only after getting your explicit consent. Please find the list of personal data we collect and the purposes thereof."
        ]:

            pdf.set_x(left_margin)
            y_offset = 2  # Adjust for best vertical alignment

            pdf.rect(left_margin, pdf.get_y() + y_offset, checkbox_size, checkbox_size)

            tick_image_path = "static/assets/img/logo/images_tick.png"
            try:
                pdf.image(tick_image_path, x=left_margin + 1, y=pdf.get_y() + y_offset + 1, w=checkbox_size,
                          h=checkbox_size)
            except Exception as e:
                print(f"Error adding tick image: {e}")

            pdf.set_x(left_margin + checkbox_size + checkbox_spacing)
            pdf.multi_cell(page_width - checkbox_size - checkbox_spacing, 6, text, align="J")  # Justified text
            pdf.ln(3)  # Reduced vertical spacing

        pdf.ln(5)

        # Applicant's Signature
        # First Row (Place and Signature)
        pdf.set_x(left_margin)
        pdf.cell(40, 10, "Place: Pune, Maharashtra.", align="L", ln=False)  # Place label and value

        # Calculate x position for the signature (right side)
        signature_x = pdf.w - left_margin - 50  # Adjust 50 for signature width

        # Add Signature Image
        signature_path = 'static/assets/img/logo/Signature.png'
        signature_width = 50  # Set your desired width
        signature_height = 20  # Set your desired height (or calculate it proportionally)
        try:
            pdf.image(signature_path, x=signature_x, y=pdf.get_y() - 5, w=signature_width, h=signature_height)
        except Exception as e:
            print(f"Error adding signature image: {e}")

        pdf.ln(15)  # Move to the next line

        # Second Row (Date and Name)
        pdf.set_x(left_margin)
        pdf.cell(40, 10, "Date: " + datetime.now().strftime("%Y-%m-%d"), align="L", ln=False)  # Date label and value

        # Calculate x position for the name (right side)
        name_x = pdf.w - left_margin - 50  # Adjust 100 for Name label + input field

        pdf.set_x(name_x)  # Set x position for the name

        pdf.set_font("Arial", size=10, style="B")  # Set to bold font
        pdf.cell(40, 10, fullname, align="L", ln=False)  # Name label (bold)
        pdf.set_font("Arial", size=10)  # Reset to regular font (if needed for subsequent text)


        # Save the PDF to a file
        pdf.output(filename)
