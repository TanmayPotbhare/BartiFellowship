from classes.database import HostConfig, ConfigPaths, ConnectParam


def total_application_count(year):
    """
    This function returns the total number of applications for a given year.
    :param year: Year for which the total count is required.
    :return: Total application count as an integer.
    """
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()

    query = "SELECT COUNT(*) FROM application_page WHERE phd_registration_year=%s"
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result[0] if result else 0


def completed_applications(year):
    """
    This function returns the count of completed applications for a given year.
    :param year: Year for which the count is required.
    :return: Count of completed applications as an integer.
    """
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()

    query = """SELECT COUNT(*) 
               FROM application_page 
               WHERE form_filled = 1 AND phd_registration_year = %s"""
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result[0] if result else 0


def incomplete_applications(year):
    """
    This function returns the count of incomplete applications for a given year.
    :param year: Year for which the count is required.
    :return: Count of incomplete applications as an integer.
    """
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()

    query = """SELECT COUNT(*) 
               FROM application_page 
               WHERE form_filled = 0 AND phd_registration_year = %s"""
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result[0] if result else 0


def accepted_applications(year):
    """
    This function returns the count of accepted applications for a given year.
    :param year: Year for which the count is required.
    :return: Count of accepted applications as an integer.
    """
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()

    query = """SELECT COUNT(*) 
               FROM application_page 
               WHERE final_approval = 'accepted' AND phd_registration_year = %s"""
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result[0] if result else 0


def rejected_applications(year):
    """
    This function returns the count of rejected applications for a given year.
    :param year: Year for which the count is required.
    :return: Count of rejected applications as an integer.
    """
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()

    query = """
               SELECT COUNT(*) 
               FROM application_page 
               WHERE phd_registration_year = %s  
               AND final_approval = 'rejected' 
               OR scrutiny_status = 'rejected' 
               OR status = 'rejected'
            """
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result[0] if result else 0


def male_applications(year):
    """
    This function returns the count of rejected applications for a given year.
    :param year: Year for which the count is required.
    :return: Count of rejected applications as an integer.
    """
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()

    query = """
               SELECT COUNT(*) 
               FROM application_page 
               WHERE phd_registration_year = %s  
               AND gender = 'Male'
            """
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result[0] if result else 0


def female_applications(year):
    """
    This function returns the count of rejected applications for a given year.
    :param year: Year for which the count is required.
    :return: Count of rejected applications as an integer.
    """
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()

    query = """
               SELECT COUNT(*) 
               FROM application_page 
               WHERE phd_registration_year = %s  
               AND gender = 'Female'
            """
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result[0] if result else 0


def disabled_applications(year):
    """
    This function returns the count of rejected applications for a given year.
    :param year: Year for which the count is required.
    :return: Count of rejected applications as an integer.
    """
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()

    query = """
               SELECT COUNT(*) 
               FROM application_page 
               WHERE phd_registration_year = %s  
               AND disability = 'Yes'
            """
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result[0] if result else 0


def notdisabled_applications(year):
    """
    This function returns the count of rejected applications for a given year.
    :param year: Year for which the count is required.
    :return: Count of rejected applications as an integer.
    """
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()

    query = """
               SELECT COUNT(*) 
               FROM application_page 
               WHERE phd_registration_year = %s  
               AND disability = 'No'
            """
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result[0] if result else 0


# def pvtg_applications():
#     """
#     This function returns the count of rejected applications for a given year.
#     :param year: Year for which the count is required.
#     :return: Count of rejected applications as an integer.
#     """
#     host = HostConfig.host
#     connect_param = ConnectParam(host)
#     cnx, cursor = connect_param.connect(use_dict=True)

#     query = """
#                SELECT *
#                FROM application_page 
#                WHERE pvtg='Yes'
#                AND pvtg_caste in ('Katkari', 'Kolam', 'Madia')
#             """
#     cursor.execute(query,)
#     result = cursor.fetchall()
#     cursor.close()
#     cnx.close()
#     return result


def get_individual_counts_pvtg():
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect(use_dict=True)

    # Query to get individual counts for each caste
    query_katkari = "SELECT COUNT(*) as count FROM application_page WHERE pvtg='Yes' AND pvtg_caste='Katkari'"
    query_kolam = "SELECT COUNT(*) as count FROM application_page WHERE pvtg='Yes' AND pvtg_caste='Kolam'"
    query_madia = "SELECT COUNT(*) as count FROM application_page WHERE pvtg='Yes' AND pvtg_caste='Madia'"

    # Execute queries and fetch counts
    cursor.execute(query_katkari)
    katkari = cursor.fetchone()['count']

    cursor.execute(query_kolam)
    kolam = cursor.fetchone()['count']

    cursor.execute(query_madia)
    madia = cursor.fetchone()['count']

    cursor.close()
    cnx.close()

    return katkari, kolam, madia


def get_individual_counts_faculty(year):
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect(use_dict=True)

    try:
        # Query to get individual counts for each faculty
        query_Science = """
            SELECT COUNT(*) as count 
            FROM application_page 
            WHERE phd_registration_year = %s AND faculty = 'Science'
        """
        query_Arts = """
            SELECT COUNT(*) as count 
            FROM application_page 
            WHERE phd_registration_year = %s AND faculty = 'Arts'
        """
        query_Commerce = """
            SELECT COUNT(*) as count 
            FROM application_page 
            WHERE phd_registration_year = %s AND faculty = 'Commerce'
        """
        query_Other = """
            SELECT COUNT(*) as count 
            FROM application_page 
            WHERE phd_registration_year = %s AND faculty = 'Other'
        """

        # Execute queries with the provided year
        cursor.execute(query_Science, (year,))
        science = cursor.fetchone()['count']

        cursor.execute(query_Arts, (year,))
        arts = cursor.fetchone()['count']

        cursor.execute(query_Commerce, (year,))
        commerce = cursor.fetchone()['count']

        cursor.execute(query_Other, (year,))
        other = cursor.fetchone()['count']

    except Exception as e:
        print(f"An error occurred while fetching counts: {e}")
        science, arts, commerce, other = 0, 0, 0, 0  # Default values in case of an error
    finally:
        # Ensure resources are closed properly
        cursor.close()
        cnx.close()

    return science, arts, commerce, other






