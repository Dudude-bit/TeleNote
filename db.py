import mysql.connector


def create_connection() :
    connection = None
    try :
        connection = mysql.connector.connect(
            host='eu-cdbr-west-03.cleardb.net',
            user='b6df603d349c62',
            passwd='731e8348',
            database='heroku_24306a1d51229cb'
        )
        connection.autocommit = True
    except mysql.connector.Error as e :
        print(e)
    return connection


def create_note(connection: mysql.connector.connection.MySQLConnection, note_title, note_text, user_id) :
    cursor = connection.cursor()
    query = f"""
    INSERT INTO note (title, note, user_id) VALUES ('{note_title}', '{note_text}','{user_id}')
    """
    cursor.execute(query)


def get_notes(connection: mysql.connector.connection.MySQLConnection, user_id) :
    cursor = connection.cursor()
    query = f"""
    SELECT * FROM note WHERE user_id = {user_id}
    """
    cursor.execute(query)
    notes = cursor.fetchall()
    return notes


def get_one_note(connection, note_id) :
    cursor = connection.cursor()
    query = f"""
    SELECT * FROM note WHERE note_id = {note_id}
    """
    cursor.execute(query)
    note = cursor.fetchall()[0]
    return note


def delete_all_notes(connection, user_id) :
    cursor = connection.cursor()
    query = f"""
    DELETE FROM note WHERE user_id = {user_id}
    """
    cursor.execute(query)


def search_notes(connection, searching_query) :
    cursor = connection.cursor()
    query = f"""
    SELECT * FROM note WHERE title LIKE '%{searching_query}%' OR note LIKE '%{searching_query}%'
    """
    cursor.execute(query)
    notes = cursor.fetchall()
    return notes
