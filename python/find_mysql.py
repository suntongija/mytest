import pymysql.cursors

class connect_mysql:
    #def __init__(self):

    def find_sha1(self, sha1):
        # Connect to the database
        connection = pymysql.connect(user='tester',
                                     host='139.9.66.126',
                                     password='123qqq...A',
                                     db='test',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:

            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `id`, `class` FROM `member` WHERE `name`=%s"
                cursor.execute(sql, (sha1,))
                result = cursor.fetchone()
                return  result
        finally:
            connection.close()
if __name__ == '__main__':
    sha1 = 'yaoyao'
    output = connect_mysql().find_sha1(sha1)
    print(output)
