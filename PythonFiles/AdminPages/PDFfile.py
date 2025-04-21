import datetime
from flask import request
from fpdf import FPDF


def get_base_url():
    base_url = request.url_root
    return base_url

def generate_award_letter(data, filename):
    # TO display the award letter for the candidates who have been awarded the Award Letter by the Admin.
    class PDF(FPDF):
        header_added = False  # To track whether the header is added to the first page

        def header(self):
            if not self.header_added:
                var = get_base_url()
                print(var)
                # Add a header
                self.set_font("Arial", "B", 10)
                # self.image('static/Images/satya.png', 94, 10, 15)
                self.image('/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/admin_assets/images/b-r-ambedkar.png', 94, 10, 15)
                # Replace with the path to your small imag
                # Calculate the width of the image
                image_width = 100  # Assuming the width of the image is 100 (adjust if different)
                # Calculate the position for "Government of Maharashtra" text
                text_x_position = self.get_x()  # Get current X position
                text_y_position = self.get_y() + 20  # Set Y position below the image
                # Set cursor position
                self.set_xy(text_x_position, text_y_position)
                # self.image('static/assets/img/logo/mahashasan.jpeg', 10, 25, 20)
                self.image('/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/assets/img/logo/barti_new.png', 10, 25,20)
                # Replace with the path to your symbol image
                # self.image('static/assets/img/logo/barti_new.png', 180, 28, 20)
                self.image('/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/Images/satya.png', 180, 23,20)
                # Replace with the path to your symbol image
                # self.ln(1)
                # self.ln(0)  # Reduce the space below the address
                self.cell(0, 5, "DR. BABASAHEB AMBEDKAR RESEARCH & TRAINING INSTITUTE (BARTI), PUNE", align="C", ln=True)

                self.ln(1)
                self.set_font("Arial", size=7)
                self.cell(0, 0, "(An Autonomous Institute of the Department of Social Justice and Special Assistance, Government of Maharashtra)", align="C", ln=True)

                self.ln(5)
                self.set_font("Arial", size=7)
                self.cell(0, 7, "Office: 28, Queens Garden, Pune - 411001.", align="C", ln=True)
                self.line(10, self.get_y(), 200, self.get_y())
                self.set_font("Arial", size=7)
                self.cell(0, 7, "TEL No.: 020-26343600/263333330/263333339   Website.: www.barti.in    Email.: dg@barti.in", align="C", ln=True)
                self.line(10, self.get_y(), 200, self.get_y())

                self.ln(3)  # Adjust this value to control the space after the line
                self.set_font("Arial", "", size=10)
                outward = data['outward_number']
                datetimes = datetime.datetime.today()
                date = datetimes.date()
                self.cell(0, 10,f"Outward Number.: {outward}", ln=False)
                self.cell(0, 10, f"Date: {date}", align="R", ln=True)
                self.ln(2)  # Adjust this value to control the space after the line

                # Define rectangle coordinates and dimensions
                x_rect = 10
                y_rect = 70
                width_rect = 190
                height_rect = 20

                # Draw the rectangle
                pdf.rect(x_rect, y_rect, width_rect, height_rect)

                # Define starting x-coordinate for the points
                x_point = x_rect + 5
                y_point = y_rect + 7
                point_spacing = 4

                # Add the points (numbers) inside the rectangle
                pdf.text(x_point, y_point, "Reference:")
                pdf.text(x_point, y_point + point_spacing, "1. Government Resolution Dated 10/09/2024 2. List of Provisionally Selected Candidate for BANRF-2022")
                pdf.text(x_point, y_point + 2 * point_spacing, "2. Dated 27/11/2024 Board of Governance Meeting 36,Subject No. 8 approval")

                self.rotate(45)  # Rotate the text by 45 degrees
                self.set_font('Arial', '', 45)
                self.set_text_color(192, 192, 192)
                self.text(-70, 210, "")  # Use text instead of rotated_text
                self.rotate(0)  # Reset the rotation to 0 degrees

                self.header_added = True  # Set to True after adding the header

        def to_name(self, data):
            self.ln(24)
            self.set_font("Arial", "", size=10)
            subject_text = "Subject: Dr. Babasaheb Ambedkar National Research Fellowship (BANRF)-2022 for Scheduled Caste candidate to pursue Ph.D. Degree"
            # Use multi_cell to handle wrapping, adjust width as needed
            self.multi_cell(0, 5, subject_text)
            self.ln(5)  # Add some space after the subject

            # "Dear Candidate,"
            name = data['first_name'] + ' ' + data['middle_name'] + ' ' + data['last_name']
            self.set_font("Arial", "B", size=11)
            self.cell(0, 10, f"Dear {name},", ln=True)

        def insert_static_data(self, data):
            # Insert your static data here
            self.ln(3)
            self.cell(0,10, " Congratulations!! ", ln=True)
            self.set_font("Arial", "", 10)
            registration_year = data['phd_registration_year']
            fiscal_year = f"BANRF - {registration_year}"
            first_para = (
                "       With reference to your application for the Research Fellowship for Scheduled Caste "
                "Candidate, I am happy to inform you that, Dr. Babasaheb Ambedkar Research and Training "
                "Institute (BARTI), Pune has selected you for Dr. Babasaheb Ambedkar National Research "
                f"Fellowship (BANRF) {registration_year} (here is after referred to as ({fiscal_year})). "
                "The financial assistance under the fellowship is awarded to you for the research subject "
                "mentioned in your registration letter submitted by you. The fellowship award is subject "
                "to genuineness of documents submitted by you and your compliance to the terms & conditions of BARTI."
            )
            second_para = (
                "Please note that all benefits are entitled as per the Social Justice and Special assistance department"
                "Government of Maharashtra Government Resolution No. SJS-2024/p.n no 77/dated 10/09/2024. "
                "You will eligible for financial assistance, relevant to you, as per the UGC regulation and norms."
            )
            third_para = (
                "Please note that, the fellowship amount and other financial assistance, as per your eligibility, "
                "stream wise, shall be disbursed through your savings Bank Account (SBI)."
            )
            fourth_para = (
                "Please note that this award letter is being issued on the basis of photocopies of the following" 
                f"documents furnished by you to BANRF-{registration_year}."
            )
            fifth_para = (
                 "1. Photocopy of your registration document for regular and full time Ph.D.course in a University / "
                 "Institution which is included & declared fit to receive financial assistance under Sec.2 (f) "
                 "and 12 B of the UGC Act 1956;"
            )
            sixth_para = (
                 "2. The photo copies of other relevant documents, pertaining to you."
            )
            seventh_para = (
                 "Please note that, you are required to submit the following documents to the designated authority "
                 "of BARTI at the stipulated time period/interval:"
            )
            eighth_para = (
                 "1. Half yearly progress report in the prescribed Performa."
            )
            nine = (
                "2. Details of the expenditure incurred out of the contingency grant to be submitted annually in"
                "the prescribed proforma."
            )
            ten = (
                "3. The claim toward HRA is subject to the submission of HRA certificate in the prescribed proforma."
            )
            eleven = (
                "4. After the completion of two years in case of Ph.D. an 'Upgradation Certificate' need to be"
                "submitted in the prescribed proforma along with progress report"
            )
            twelve = (
                "Please note that this award is subject to your acceptance of all the terms and conditions of BARTI"
                "and subject to submitting an undertaking to that effect, on receipt of this Award Letter."
            )
            thirteen = (
                "Please note that the award letter is provisional and will be treated as valid, subject to submission" 
                "of undertaking mentioned above and also subject to the geniuses of the documents submitted by you."
            )
            fourteen = (
                "Dr. Babasaheb Ambedkar Research and Training Institute reserves all the rights to add terms and" 
                "conditions as an when required and candidates have to accept the changes in the terms and conditions" 
                "of the fellowship. In case of dispute regarding the fellowship, the Director General of BARTI, will be" 
                "the final authority. Candidates who have previously benefited under BANRF for M.Phil and selected for" 
                f"BANRF-{registration_year} Ph.D. course the tenure of fellowship will be 3 years as per mentioned in BANRF-{registration_year}" 
                "guidelines."
            )
            fifteen = (
                "We hope this fellowship will help you financially and academically conduct research on your subject" 
                "and develop yourself an academic excellence. It will help you to grow not just as researcher but also a"
                "champion for the cause of equality, social justice and contributor to the peace, harmony and happiness" 
                "among the various disadvantaged sections of society."
            )
            sixteen = (
                "BARTI wishes you all the best in this endeavor."
            )
            seventeen = (
                "Once again, all the Best Wishes for a bright future ........!!!!"
            )
            self.multi_cell(0, 7, first_para)
            self.ln(2)  # Adjust this value to control the space before static data
            self.multi_cell(0, 7, second_para)
            self.ln(2)  # Adjust this value to control the space before static data
            self.multi_cell(0, 7, third_para)
            self.ln(2)  # Adjust this value to control the space before static data
            self.multi_cell(0, 7, fourth_para)
            self.ln(2)  # Adjust this value to control the space before static data
            self.multi_cell(0, 7, fifth_para)
            self.ln(2)  # Adjust this value to control the space before static data
            self.multi_cell(0, 7, sixth_para)
            self.ln(19)  # Adjust this value to control the space before static data
            self.multi_cell(0, 7, seventh_para)
            self.ln(2)  # Adjust this value to control the space before static data
            self.multi_cell(0, 7, eighth_para)
            self.multi_cell(0, 7, nine)
            self.multi_cell(0, 7, ten)
            self.multi_cell(0, 7, eleven)
            self.ln(4)  # Adjust this value to control the space before static data
            self.multi_cell(0, 7, twelve)
            self.ln(2)  # Adjust this value to control the space before static data
            self.multi_cell(0, 7, thirteen)
            self.ln(2)  # Adjust this value to control the space before static data
            self.multi_cell(0, 7, fourteen)
            self.ln(2)  # Adjust this value to control the space before static data
            self.multi_cell(0, 7, fifteen)
            self.ln(2)  # Adjust this value to control the space before static data
            self.multi_cell(0, 7, sixteen)
            self.ln(2)  # Adjust this value to control the space before static data
            self.multi_cell(0, 7, seventeen)

            self.set_x(150)  # Adjust the x-coordinate as needed

            self.ln(1)
            self.cell(160,10, "With Regards,", align='R', ln=True)
            # self.image('static/assets/img/logo/signHOD.png', 140, 187, 30)
            self.image('/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/assets/img/logo/signHOD.png', 140, 187, 30)
            self.ln(12)
            self.cell(165, 5, "(Umesh Sonawane)", align='R', ln=True)
            self.cell(165, 5, "Head of Department", align='R', ln=True)
            self.cell(180, 5, "Dr. Babasaheb Ambedkar Research &", align='R', ln=True)
            self.cell(177, 5, "Training Institute, (BARTI), Pune.", align='R', ln=True)
            # self.image('static/Images/sonanwanesir_signature.png',  125, 210, 50)
            # self.image('/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/Images/sonanwanesir_signature.png', 125, 210, 50)
            self.ln(5)  # Adjust this value to control the space after static data

        def footer(self):
            # Add a footer
            self.set_y(-15)
            self.set_font("arial", "B", 8)
            self.cell(0, 10, f" {self.page_no()} ", align="C")

            # Center-align the "TRTI" text
            self.cell(0, 10, " BARTI  |  Fellowship ", align="R")

    def add_page_borders(pdf, margin=10, color=(0, 0, 0), line_width=1):
        """
        Adds a rectangular border around the page with customizable color and line width.

        Args:
            pdf: The PDF object.
            margin: The margin (in points) from the page edges.
            color: A tuple (r, g, b) representing the border color (0-255).
            line_width: The width of the border line in points.
        """
        page_width = pdf.w
        page_height = pdf.h

        pdf.set_draw_color(*color)  # Set the border color
        pdf.set_line_width(line_width)  # Set the border line width

        pdf.rect(margin, margin, page_width - 2 * margin, page_height - 2 * margin)

    pdf = PDF(orientation='P', format='A4')
    pdf.add_page()
    pdf.header()
    pdf.to_name(data)

    border_margin = 5
    border_color = (0, 0, 0)  # Red border
    border_line_width = 1
    # add_page_borders(pdf, margin=border_margin, color=border_color, line_width=border_line_width)

    # Insert static data
    pdf.insert_static_data(data)
    # Save the PDF to a file
    pdf.output(filename)


# This below function (generate_pdf_with_styling) is used on fellowship_awarded.html Page
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
                self.image('/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/assets/img/logo/barti_new.png', 10, 10, 23)
                self.image('/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/assets/img/logo/diya.png', 175, 10, 23)
                self.image('/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/admin_assets/images/b-r-ambedkar.png', 95, 10, 13)  # Center the image

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
                         f"Fellowship BANRF {int(fellowship_year)}",
                         align="C", ln=True, fill=True)
                # ------------------- Blue Box -----------------------
                self.ln(2)  # Adjust this value to control the space after the line

                # ----------------------------------------------------
                # Image Alignment and Call
                self.ln(1)
                image_x = 173  # Adjust this to place the image further to the right if needed
                image_y = self.get_y()  # Current y-position of the cursor after the blue box
                # Insert the image to the right
                photo = '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship' + data['applicant_photo']
                # photo = '/static/assets/img/leaders/ajitpawar.jpg'
                # modified_path = photo[1:] if photo.startswith("/") else photo
                # Define image size (width, height)
                image_width = 25
                image_height = 25
                # Draw a rectangle border around the image
                border_padding = 2  # Padding around the image within the border
                self.set_draw_color(0, 0, 0)  # Set border color to black
                self.rect(image_x - border_padding, image_y - border_padding, image_width + 2 * border_padding,
                          image_height + 2 * border_padding)  # Draw border around the image
                # Insert the image inside the border
                self.image(photo, image_x, image_y, image_width, image_height)
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
                    ("Applicant ID:",
                     f"BARTI/BANRF{data.get('phd_registration_year', 'XXXX')}/{data.get('id', 'XXXX')}"),
                    ("Full Name:",
                     f"{data.get('first_name', '')} {data.get('middle_name', '')} {data.get('last_name', '')}"),
                    ("Submitted Date:", str(data.get('application_date', 'N/A')) + ' ' + '(YYYY-MM-DD)'),
                    ("Submitted Time:", str(data.get('application_time', 'N/A')) + ' ' + '(HH:MM:SS)')
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
        "Date of Birth:": str(data['date_of_birth']) + ' ' + '(YYYY-MM-DD)',
        "Gender:": data['gender'],
        "Age:": str(data['age']) + ' ' + 'Years',
        "Category:": 'Scheduled Caste',
        "Caste: ": data['your_caste'],
        "Salaried": data['salaried'],
        "Disability": data['disability']
        # Add more fields as needed
    }

    if 'disability' in data and data['disability'] == 'Yes':
        personal_details["Type of Disability:"] = data['type_of_disability']

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
        "SSC Attempts:": str(data['ssc_attempts']) + ' ' + 'Attempt',
        "SSC Total Marks:": str(data['ssc_total']) + ' ' + '(Obtained Marks)',
        "SSC Percentage:": str(data['ssc_percentage']) + '%'
    }

    hsc = {
        "HSC Passing Year:": data['hsc_passing_year'],
        "HSC School Name:": data['hsc_school_name'],
        "HSC Stream:": data['hsc_stream'],
        "HSC Attempts:": str(data['hsc_attempts']) + ' ' + 'Attempt',
        "HSC Total Marks:": str(data['hsc_total']) + ' ' + '(Obtained Marks)',
        "HSC Percentage:": str(data['hsc_percentage']) + '%'
    }

    grad = {
        "Graduation Passing Year:": data['graduation_passing_year'],
        "Graduation College Name:": data['graduation_school_name'],
        "Graduation Stream:": data['grad_stream'],
        "Graduation Attempts:": str(data['grad_attempts']) + ' ' + 'Attempt',
        "Graduation Total Marks:": str(data['grad_total']) + ' ' + '(Obtained Marks)',
        "Graduation Percentage:": str(data['graduation_percentage']) + '%'
    }

    postgrad = {
        "Post Grad. Passing Year:": data['phd_passing_year'],
        "Post Grad. College Name:": data['phd_school_name'],
        "Post Grad. Stream:": data['pg_stream'],
        "Post Grad. Attempts:": str(data['pg_attempts']) + ' ' + 'Attempt',
        "Post Grad. Total Marks:": str(data['pg_total']) + ' ' + '(Obtained Marks)',
        "Post Grad. Percentage:": str(data['phd_percentage']) + '%',
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
        "P.H.D Registration Date:": str(data['phd_registration_date']) + ' ' + '(YYYY-MM-DD)',
        "P.H.D Registration Year:": data['phd_registration_year'],
        "Age at Ph.D. Registration:": str(data['phd_registration_age']) + ' ' + 'Years',
        "Fellowship Application Year:": 'STRF' + ' ' + data['fellowship_application_year'],
        "Department Name:": data['department_name'],
        "Topic of Ph.D.:": data['topic_of_phd'],
        "Name of Guide:": data['name_of_guide'],
        "Faculty/Stream:": data['faculty'],
        "District of Research Center": data['research_center_district']
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
        "Family Annual Income:": 'INR' + ' ' + str(data['family_annual_income']),
    }
    if 'income_certificate_number' in data and data['income_certificate_number'] in ['', None]:
        income_details["Income Certificate Present:"] = 'No Certificate'
        income_details["Income Certificate Issue Date:"] = data['income_barcode_issue_date'] + ' ' + '(YYYY-MM-DD)'
        income_details["Income Certificate Issuing Authority:"] = data['issuing_authority']
        income_details["Income Certificate Issuing District:"] = data['income_issuing_district']
        income_details["Income Certificate Issuing Taluka:"] = data['income_issuing_taluka']
    else:
        income_details["Income Certificate Present:"] = 'Yes'
        income_details["Income Certificate Number:"] = data['income_certificate_number']
        income_details["Income Certificate Issuing Authority:"] = data['issuing_authority']
        income_details["Income Certificate Issuing District:"] = data['income_issuing_district']
        income_details["Income Certificate Issuing Taluka:"] = data['income_issuing_taluka']

    domicile_details = {
        "Are you Domicile of Maharashtra:": data['domicile'],
    }
    if 'domicile_number' in data and data['domicile_number'] in ['', None]:
        domicile_details["Domicile Certificate Present:"] = 'No Certificate'
        domicile_details["Domicile Certificate Issue Date:"] = data[
                                                                   'domicile_barcode_issue_date'] + ' ' + '(YYYY-MM-DD)'
        domicile_details["Domicile Certificate Issuing Authority:"] = data['domicile_issuing_authority']
        domicile_details["Domicile Certificate Issuing District:"] = data['domicile_issuing_district']
        domicile_details["Domicile Certificate Issuing Taluka:"] = data['domicile_issuing_taluka']
    else:
        domicile_details["Domicile Certificate Present:"] = 'Yes'
        domicile_details["Domicile Certificate Number:"] = data['domicile_number']
        domicile_details["Domicile Certificate Issuing Authority:"] = data['domicile_issuing_authority']
        domicile_details["Domicile Certificate Issuing District:"] = data['domicile_issuing_district']
        domicile_details["Domicile Certificate Issuing Taluka:"] = data['domicile_issuing_taluka']

    caste_details = {
        "Do you have Caste Certificate:": data['caste_certf'],
    }
    if 'caste_certf_number' in data and data['caste_certf_number'] in ['', None]:
        caste_details["Caste Certificate Present:"] = 'No Certificate'
        caste_details["Caste Certificate Issue Date:"] = data['caste_barcode_issue_date'] + ' ' + '(YYYY-MM-DD)'
        caste_details["Caste Certificate Issuing Authority:"] = data['caste_issuing_authority']
        caste_details["Caste Certificate Issuing District:"] = data['issuing_district']
        caste_details["Caste Certificate Issuing Taluka:"] = data['caste_issuing_taluka']
    else:
        caste_details["Caste Certificate Present:"] = 'Yes'
        caste_details["Caste Certificate Number:"] = data['caste_certf_number']
        caste_details["Caste Certificate Issuing Authority:"] = data['caste_issuing_authority']
        caste_details["Caste Certificate Issuing District:"] = data['issuing_district']
        caste_details["Caste Certificate Issuing Taluka:"] = data['caste_issuing_taluka']

    validity_details = {
        "Do you have Validity Certificate:": data['validity_certificate'],
    }
    if 'validity_certificate' in data and data['validity_certificate'] == 'Yes':
        if 'validity_cert_number' in data and data['validity_cert_number'] in ['', None]:
            validity_details["Validity Certificate Present:"] = 'No Certificate'
            validity_details["Validity Certificate Issue Date:"] = data[
                                                                       'validity_barcode_issue_date'] + ' ' + '(YYYY-MM-DD)'
            validity_details["Validity Certificate Issuing Authority:"] = data['validity_issuing_authority']
            validity_details["Validity Certificate Issuing District:"] = data['validity_issuing_district']
            validity_details["Validity Certificate Issuing Taluka:"] = data['validity_issuing_taluka']
        else:
            validity_details["Validity Certificate Present:"] = 'Yes'
            validity_details["Validity Certificate Number:"] = data['validity_cert_number']
            validity_details["Validity Certificate Issuing Authority:"] = data['validity_issuing_authority']
            validity_details["Validity Certificate Issuing District:"] = data['validity_issuing_district']
            validity_details["Validity Certificate Issuing Taluka:"] = data['validity_issuing_taluka']
    else:
        pass

    parent_details = {
        "Father Name:": data['father_name'],
        "Mother Name:": data['mother_name'],
        "Anyone Work in Government:": data['work_in_government'],
        "IFSC Code:": data['ifsc_code'],
        "Account Number:": data['account_number'],
        "Bank Name:": data['bank_name'],
        "Account Holder Name:": data['account_holder_name'],
        "MICR Code:": data['micr']
    }

    signature_doc = data.get('signature')
    adhaar_doc = data.get('adhaar_card_doc')
    pan_doc = data.get('pan_card_doc')
    domicile_doc = data.get('domicile_doc')
    caste_doc = data.get('caste_doc')
    validity_doc = data.get('validity_doc')
    income_doc = data.get('income_doc')
    ssc_doc = data.get('ssc_doc')
    hsc_doc = data.get('hsc_doc')
    grad_doc = data.get('grad_doc')
    postgrad_doc = data.get('post_grad_doc')
    entrance_doc = data.get('entrance_doc')
    phd_reciept_doc = data.get('phd_reciept_doc')
    # guideAllotment_doc = data.get('guideAllotment_doc')
    # guideAccept_doc = data.get('guideAccept_doc')
    # rac_doc = data.get('rac_doc')
    confirmation_doc = data.get('confirmation_doc')
    joining_doc = data.get('joining_doc')
    annexureA_doc = data.get('annexureA_doc')
    annexureB_doc = data.get('annexureB_doc')
    annexureC_doc = data.get('annexureC_doc')
    annexureD_doc = data.get('annexureD_doc')
    disable_doc = data.get('disable_doc')
    gazete_doc = data.get('gazete_doc')
    # selfWritten_doc = data.get('selfWritten_doc')
    research_letter_doc = data.get('research_letter_doc')

    def is_document_present(doc_value):
        """
        Checks if a document is considered present based on various criteria.

        Args:
            doc_value: The value associated with the document (e.g., filename, path, or boolean).

        Returns:
            True if the document is considered present, False otherwise.
        """
        if doc_value is None:
            return False
        if isinstance(doc_value, str) and doc_value.strip() == "":  # Check for empty string
            return False
        if isinstance(doc_value, str) and doc_value == "Save File":  # Check for "SAVE FILE" (case-insensitive)
            return False
        if isinstance(doc_value, bool):  # If it's already a boolean
            return doc_value
        return True  # Default to True if none of the above conditions are met

    doc_uploaded = {
        "Signature": is_document_present(signature_doc),
        "Adhaar Card": is_document_present(adhaar_doc),
        "Pan Card": is_document_present(pan_doc),
        "Domicile Certificate": is_document_present(domicile_doc),
        "Caste Certificate": is_document_present(caste_doc),
        "Validity Certificate": is_document_present(validity_doc),
        "Income Certificate": is_document_present(income_doc),
        "Secondary School Certificate": is_document_present(ssc_doc),
        "Higher Secondary Certificate": is_document_present(hsc_doc),
        "Graduation Certificate": is_document_present(grad_doc),
        "Post Graduation Certificate": is_document_present(postgrad_doc),
        "SET/GATE/CET Marksheet & Passing Certificate": is_document_present(entrance_doc),
        "Ph.D Admission Reciept": is_document_present(phd_reciept_doc),
        # "Guide Allotment Letter": is_document_present(guideAllotment_doc),
        # "Guide Acceptance Letter": is_document_present(guideAccept_doc),
        # "Letter of Accpetance from RAC/RRC": is_document_present(rac_doc),
        "Confirmation Letter": is_document_present(confirmation_doc),
        "Research Center Joining Report": is_document_present(joining_doc),
        "Annexure A - Self Declaration": is_document_present(annexureA_doc),
        "Annexure B - Undertaking": is_document_present(annexureB_doc),
        "Annexure C - Affidavit": is_document_present(annexureC_doc),
        "Annexure D - Non Beneficiary Certificate": is_document_present(annexureD_doc),
        "Disability Certificate": is_document_present(disable_doc),
        "Change in Name - Gazzette": is_document_present(gazete_doc),
        # "Self Written Certificate of not getting scholarship from anywhere": is_document_present(selfWritten_doc),
        "Research Synopsis/ Research Center Allotment letter": is_document_present(research_letter_doc),
    }

    pdf = PDF(orientation='P', format='A4')
    pdf.add_page()
    pdf.header()
    # pdf.image_and_date(data)

    # ---------------------- Section 1 - Personal Details ----------------
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
    pdf.set_font("Arial", size=10)  # Decreased font size
    pdf.ln(2)

    # Set the left margin to ensure proper alignment
    left_margin = 10
    col_widths = [90, 90]  # Adjust column widths as needed
    x_start = left_margin
    line_height = 4  # Decreased line height

    perm_address_data = list(address_details.items())
    print(perm_address_data)
    comm_address_data = list(com_address_details.items())

    max_rows = max(len(perm_address_data), len(comm_address_data))

    for i in range(max_rows):
        pdf.set_x(x_start)
        current_y = pdf.get_y()
        max_label_height_perm = line_height
        max_value_height_perm = line_height
        max_label_height_comm = line_height
        max_value_height_comm = line_height

        # Permanent Address
        if i < len(perm_address_data):
            label, value = perm_address_data[i]
            pdf.multi_cell(col_widths[0] / 2, line_height, label, align="L")
            label_height_perm = pdf.get_y() - current_y
            max_label_height_perm = max(max_label_height_perm, label_height_perm)

            pdf.set_xy(x_start + col_widths[0] / 2, current_y)
            pdf.multi_cell(col_widths[0] / 2, line_height, str(value), align="L")
            value_height_perm = pdf.get_y() - current_y
            max_value_height_perm = max(max_value_height_perm, value_height_perm)
        else:
            pdf.cell(col_widths[0] / 2, line_height, "", align="L")
            pdf.cell(col_widths[0] / 2, line_height, "", align="L")

        # Communication Address
        pdf.set_xy(x_start + col_widths[0], current_y)
        if i < len(comm_address_data):
            label, value = comm_address_data[i]
            pdf.multi_cell(col_widths[1] / 2, line_height, label, align="L")
            label_height_comm = pdf.get_y() - current_y
            max_label_height_comm = max(max_label_height_comm, label_height_comm)

            pdf.set_xy(x_start + col_widths[0] + col_widths[1] / 2, current_y)
            pdf.multi_cell(col_widths[1] / 2, line_height, str(value), align="L")
            value_height_comm = pdf.get_y() - current_y
            max_value_height_comm = max(max_value_height_comm, value_height_comm)
        else:
            pdf.cell(col_widths[1] / 2, line_height, "", align="L")
            pdf.cell(col_widths[1] / 2, line_height, "", align="L")

        # Move to the next line, taking the maximum height of the current row
        pdf.ln(max(max_label_height_perm, max_value_height_perm, max_label_height_comm, max_value_height_comm))

    pdf.ln(9)
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
    pdf.set_font("Arial", "B", size=10)
    pdf.ln(2)

    pdf.cell(0, 10, "S.S.C Details", ln=True)
    pdf.set_font("Arial", size=10)
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

    pdf.ln(9)
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
             f"Domicile Details",
             align="C", ln=True, fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10)
    pdf.ln(2)

    # Set the left margin to ensure proper alignment
    left_margin = 10  # Margin for left alignment
    key_width = 70  # Fixed width for keys
    value_width = 30  # Remaining width for values (adjust as needed)

    key_value_spacing = 5  # Space between key-value pairs
    for key, value in domicile_details.items():
        pdf.set_x(left_margin)  # Set x position to ensure left alignment
        pdf.cell(key_width, key_value_spacing, key, align="L", ln=False)  # Print the key
        # Print the value (with remaining width)
        pdf.cell(value_width, key_value_spacing, str(value), align="L", ln=True)  # Print the value

    pdf.ln(5)
    # ----------------------- END Section 5 ---------------------------------

    # ---------------------- Section 5 - Income Details ----------------
    if pdf.get_y() > 270:  # Prevent overflow
        pdf.add_page()
    pdf.set_fill_color(0, 0, 139)  # Dark blue RGB
    # Set the text color to white
    pdf.set_text_color(255, 255, 255)  # White color
    # Add the text inside the box
    pdf.cell(0, 10,
             f"Caste Details",
             align="C", ln=True, fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10)
    pdf.ln(2)

    # Set the left margin to ensure proper alignment
    left_margin = 10  # Margin for left alignment
    key_width = 70  # Fixed width for keys
    value_width = 30  # Remaining width for values (adjust as needed)

    key_value_spacing = 5  # Space between key-value pairs
    for key, value in caste_details.items():
        pdf.set_x(left_margin)  # Set x position to ensure left alignment
        pdf.cell(key_width, key_value_spacing, key, align="L", ln=False)  # Print the key
        # Print the value (with remaining width)
        pdf.cell(value_width, key_value_spacing, str(value), align="L", ln=True)  # Print the value

    pdf.ln(5)
    # ----------------------- END Section 5 ---------------------------------

    # ---------------------- Section 5 - Income Details ----------------
    if pdf.get_y() > 270:  # Prevent overflow
        pdf.add_page()
    pdf.set_fill_color(0, 0, 139)  # Dark blue RGB
    # Set the text color to white
    pdf.set_text_color(255, 255, 255)  # White color
    # Add the text inside the box
    pdf.cell(0, 10,
             f"Validity Details",
             align="C", ln=True, fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10)
    pdf.ln(2)

    # Set the left margin to ensure proper alignment
    left_margin = 10  # Margin for left alignment
    key_width = 70  # Fixed width for keys
    value_width = 30  # Remaining width for values (adjust as needed)

    key_value_spacing = 5  # Space between key-value pairs
    for key, value in validity_details.items():
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
    image_height = 3  # Reduced image height
    image_offset_x = 2  # Offset to fine-tune horizontal position
    image_offset_y = 1  # Offset to fine-tune vertical position

    for key, value in doc_uploaded.items():
        pdf.set_x(left_margin)
        pdf.cell(key_width, key_value_spacing, key, align="L", ln=False)

        if value:
            image_path = '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/assets/img/logo/check_mark.png'
        else:
            image_path = '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/assets/img/logo/cross_icon.png'

        # print('Value of Doc:', value)

        # if value is True:
        #     image_path = "static/assets/img/logo/check_mark.png"
        # else:
        #     image_path = "static/assets/img/logo/cross_icon.png"

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

        tick_image_path = "var/www/fellowship/fellowship/BartiFellowship/BartiFellowship/static/assets/img/logo/images_tick.png"
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
    # signature_path = 'static/assets/img/logo/Signature.png'
    signature_path = '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship' + data['signature']
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
