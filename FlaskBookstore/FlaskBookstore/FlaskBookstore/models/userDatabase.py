import sqlite3, FlaskBookstore
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


class UserDbRepository(object):
    """description of class"""

    def __init__(self):
        self.__conn = sqlite3.connect(r'FlaskBookstore\data\bookstore.sqlite')


    def __del__(self):
        self.__conn.close()

    def add_user(self, username, email, password):
        try:
            cursor = self.__conn.cursor()
            cursor.execute("insert into user(userName, userEmail, password) values(?, ?, ?)", \
                                        (username, email, generate_password_hash(password)))
            self.__conn.commit()
        except Exception as e:
            print(e)

    def validate_user(self, email, password):
        try:
            cursor = self.__conn.cursor()
            userPwd = "SELECT password FROM user WHERE userEmail = '" + email + "'"
            results = cursor.execute(userPwd)
            dbresult = results.fetchone()

            dbPwd = dbresult[0]

            validPwd = check_password_hash(dbPwd, password)

            if validPwd:
                return True
            else:
                return False

        except Exception as e:
            print(e)
