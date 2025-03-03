# columns.py

# Define the columns to be used across different queries
COMMON_COLUMNS = [
    "applicant_id", "full_name", "email", "jrf_srf",
    "fellowship_awarded_year", "faculty", "date", "duration_date_from", "duration_date_to",
    "total_months", "fellowship", "total_fellowship", "hra_rate", "hra_amount",
    "hra_months", "total_hra_rate", "contingency", "pwd", "total",
    "city", "bank_name", "ifsc_code", "account_number", "quarters"
]

# Define the headers as a dictionary
COMMON_HEADERS = {
    "applicant_id": "Applicant ID",
    'full_name': "Full Name",
    'email': "Email ID ",
    'jrf_srf': "Fellowship",
    'fellowship_awarded_year': "Fellowship Awarded Year",
    'faculty': "Faculty",
    'date': "Date",
    'duration_date_from': "Duration Date From",
    'duration_date_to': "Duration Date To",
    'total_months': "Fellowship Total Months",
    'fellowship': "Fellowship",
    'total_fellowship': "Total Fellowship",
    'hra_rate': "HRA Rate",
    'hra_amount': "HRA Amount",
    'hra_months': "HRA Total Months",
    'total_hra_rate': "Total HRA Rate",
    'contingency': "Contingency",
    'pwd': "Total PWD",
    'total': "Total",
    'city': 'City',
    'bank_name': "Bank Name",
    'ifsc_code': "IFSC Code",
    'account_number': "Account Number",
    'quarters': 'Quarter'
}

