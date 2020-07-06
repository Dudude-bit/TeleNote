import mysql.connector


def create_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            db_name=123
        )
    except mysql.connector.Error as e:
        print(e)
    return connection