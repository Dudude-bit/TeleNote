import mysql.connector


def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='eu-cdbr-west-03.cleardb.net',
            user='b6df603d349c62',
            passwd='731e8348',
            database='heroku_24306a1d51229cb'
        )
    except mysql.connector.Error as e:
        print(e)
    return connection

create_connection()