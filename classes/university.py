import mysql.connector


class universityController:
    def __init__(self, host):
        self.host = host
        cnx = mysql.connector.connect(user='root1',
                                    password='Admin@#$123',
                                    host=self.host,
                                    database='BartiApplication')
        self.cursor = cnx.cursor(dictionary=True)
        self.cnx = cnx
        # self.cnx = cnx
        # self.cursor = cursor

    def get_all_university(self):
        self.cursor.execute("SELECT DISTINCT id, u_id, affiliated_universities FROM universities GROUP BY u_id")
        result = self.cursor.fetchall()
        return result

    def get_college_name(self, u_id):
        self.cursor.execute("SELECT id, u_id, college_name FROM universities where u_id =" + u_id)
        result = self.cursor.fetchall()
        return result
