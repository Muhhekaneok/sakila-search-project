import mysql.connector


def make_connection(dbconfig):
    try:
        connection = mysql.connector.connect(**dbconfig)
        cursor = connection.cursor()
        return connection, cursor
    except mysql.connector.Error as error:
        print(f"Database connection error: {error}")
        return None, None


def close_connection(connection, cursor):
    if cursor:
        cursor.close()
    if connection:
        connection.close()
