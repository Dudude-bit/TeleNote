import mysql.connector


def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=,
            user=user_name,
            passwd=user_password,
            db_name=123
        )
    except mysql.connector.Error as e:
        print(e)
    return connection