import mysqlclient.connector


def create_connection():
    connection = None
    try:
        connection = mysqlclient.connector.connect(
            host='eu-cdbr-west-03.cleardb.net',
            user='b6df603d349c62',
            passwd='731e8348',
            database='heroku_24306a1d51229cb'
        )
    except mysqlclient.connector.Error as e:
        print(e)
    return connection

connection = create_connection()