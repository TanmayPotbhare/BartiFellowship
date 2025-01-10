import mysql.connector
from classes.connection import *


class casteController:
    def __init__(self,host):
        self.host = host
        cnx = mysql.connector.connect(user=HostConfig.user, password=HostConfig.password,       # --------  DATABASE CONNECTION
                              host=self.host,
                              database=HostConfig.database)
        self.cursor = cnx.cursor(dictionary=True)
        self.cnx = cnx
        # self.cnx = cnx
        # self.cursor = cursor

    def get_all_caste_details(self):
        self.cursor.execute("""
                SELECT DISTINCT category, unique_number 
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
