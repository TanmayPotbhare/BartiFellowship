import datetime
import subprocess
import time
import json
import mysql.connector
from mysql.connector import Error
from urllib.parse import parse_qs
import datetime


# Function to connect to the database and update Aadhaar Number and Reference Number
def connect_to_database(aadhaarnum, refnum, actual_data, opr, current_date, entered_url, status):

    # Establish the connection
    connection = mysql.connector.connect(
        host='192.168.10.69',  # Database host, e.g., 'localhost'
        database='cdaclogs',  # Database name
        user='root1',  # Database user
        password='Admin@#$123'  # Database password
    )
    if connection.is_connected():
        # print("Successfully connected to the database")

        # Creating a cursor to execute queries
        cursor = connection.cursor()

        # Update Query to set refnum based on aadhaarnum
        update_query = """
            INSERT INTO adhaar_transactions (adhaar_number, reference_num, actual_data, operation, date_time, url, status) VALUES (%s, %s, %s, %s, %s, %s, %s);
        """

        # Execute the update query with parameters
        cursor.execute(update_query, (aadhaarnum, refnum, actual_data, opr, current_date, entered_url, status))
        connection.commit()  # Commit the transaction

        # print(f"Record Updated: Aadhaar Number: {aadhaarnum}, Reference Number: {refnum}")


# WSGI Application Function
def application(environ, start_response):
    try:
        # Check if the request method is GET
        if environ['REQUEST_METHOD'] == 'POST':
            # Parse the form data (assuming data is in the body)
            content_length = int(environ.get('CONTENT_LENGTH', 0))  # Get the content length from the headers
            post_data = environ['wsgi.input'].read(content_length).decode('utf-8')  # Read and decode the body

            # Parse the form data
            query_params = parse_qs(post_data)

            # Get 'entered_uid', 'entered_url', and 'entered_opr' parameter values
            entered_uid = query_params.get('entered_uid', [None])[0]
            entered_url = query_params.get('entered_url', [None])[0]
            entered_opr = query_params.get('entered_opr', [None])[0]
            entered_refnum = query_params.get('entered_refnum', [None])[0]
            # Check if 'entered_uid' and 'entered_url' were provided
            # if not entered_uid:
            #     raise ValueError("Missing 'entered_uid' parameter")
            # if not entered_url:
            #     raise ValueError("Missing 'entered_url' parameter")

            # Initialize variables for the Java command
            number = " "
            RefNum = " "

            # Conditional checks based on the 'entered_opr' parameter
            if entered_opr == 'getrefnum' and (number is None or number == ' '):
                number = entered_uid  # Set number to entered_uid if 'getrefnum' operation

            if entered_opr == 'getuid' and (RefNum is None or RefNum == ' '):
                RefNum = entered_refnum  # Set RefNum to an empty space if 'getuid' operation

            setAc = "A100098"
            setSA = "A100098"
            setLK = "260288bb-f12c-4955-a2b6-94b77f98236b"
            opr = entered_opr
            keyType = "aes"
            tokenType = "soft"
            url = "https://sp.epramaan.in:8038/vault/"
            idType = "uid"

            # Generate the current Unix timestamp in seconds
            timestamp = int(time.time())

            # Prepare the arguments array for the Java command
            args = [
                "java", "-jar", "/var/www/fellowship/fellowship/cdac/wrapper.jar",
                number, RefNum, setAc, setSA, setLK,
                opr, keyType, tokenType, url, idType, str(timestamp)
            ]

            # Run the Java command using subprocess
            process = subprocess.run(args, capture_output=True, text=True)

            # Extract the required values from the Java output (assuming 'stdout' contains refnum)
            if entered_refnum:
                refnum = RefNum
            else:
                refnum = process.stdout.split("REFNUM :")[1].split()[0].strip() # Reference Number from the Java command output

            if entered_uid:
                entered_uid = entered_uid
            else:
                entered_uid = process.stdout.split("AadhaarNumber :")[1].split()[0].strip()

            actual_data = process.stdout.strip()
            current_date = datetime.datetime.now()
            url = entered_url
            status = process.stdout.split("Status :")[1].split()[0].strip()

            # Log the Java command output for debugging
            # print("Java Command Output:", process.stdout)
            # print("Java Command Error (if any):", process.stderr)

            # Prepare the response output based on subprocess result
            output_data = {
                "stdout": process.stdout.strip(),
                "stderr": process.stderr.strip() if process.stderr else None,
                "returncode": process.returncode,
                "URL": entered_url,
                "adharnum": entered_uid,
                "refnum": refnum,
                "Status": True
            }

            # Convert the output data to JSON
            output = json.dumps(output_data).encode('utf-8')

            # Call the function to update the database with aadhaarnum and refnum
            connect_to_database(entered_uid, refnum, output, opr, current_date, entered_url, status)

            # Set response headers for JSON and CORS
            response_headers = [
                ('Content-type', 'application/json'),
                ('Content-Length', str(len(output))),
                ('Access-Control-Allow-Origin', '*'),  # Allow all origins for CORS
                ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),  # Allowed HTTP methods
                ('Access-Control-Allow-Headers', 'Content-Type')  # Allow specific headers
            ]

            # Set status and return response
            status = '200 OK'
            start_response(status, response_headers)
            return [output]

    except Exception as e:
        # Handle errors and send a 500 response
        error_output = json.dumps({"error": str(e)}).encode('utf-8')
        start_response('500 Internal Server Error', [('Content-type', 'application/json')])
        return [error_output]
