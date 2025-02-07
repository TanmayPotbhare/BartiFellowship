import mysql.connector


class casteController:
    def __init__(self, host):
        self.host = host
        cnx = mysql.connector.connect(  user='root1',
                                        password='Admin@#$123',
                                        host=self.host,
                                        database='BartiApplication')
        self.cursor = cnx.cursor(dictionary=True)
        self.cnx = cnx
        # self.cnx = cnx
        # self.cursor = cursor

    def get_all_caste_details(self):
        self.cursor.execute("""
                SELECT DISTINCT category, unique_number, caste_name
                FROM sccaste
            """)
        result = self.cursor.fetchall()
        return result

    def get_subcastes_by_unique_number(self, unique_number):
        self.cursor.execute("""
            SELECT caste_name 
            FROM sccaste 
            WHERE unique_number = %s
        """, (unique_number,))
        result = self.cursor.fetchall()
        return [row['caste_name'] for row in result]

    def get_all_caste_validity_auth(self):
        self.cursor.execute("""
                SELECT *
                FROM BartiApplication.CasteValidityAuthority
            """)
        result = self.cursor.fetchall()
        return result

    def get_taluka_from_district(self, district_id):
        self.cursor.execute("""
            SELECT taluka_name
            FROM BartiApplication.talukas
            WHERE district_id_fk = %s
        """, (district_id,))
        result = self.cursor.fetchall()
        return [row['taluka_name'] for row in result]
