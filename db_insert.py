from connection_and_close import make_connection, close_connection
from config_db_insert import dbconfig_insert


def log_search(search_type: str, search_value: str):
    connection, cursor = make_connection(dbconfig=dbconfig_insert)
    if not connection:
        return

    query = """
    INSERT INTO search_logs (search_type, search_value)
    VALUES (%s, %s);
    """
    cursor.execute(query, (search_type, search_value))
    connection.commit()

    close_connection(connection, cursor)


def get_clear_table():
    connection, cursor = make_connection(dbconfig=dbconfig_insert)
    if not connection:
        print("Failed to connect to the database")
        return

    query = "TRUNCATE TABLE search_logs;"
    cursor.execute(query)
    connection.commit()
    print("Table search_logs successfully cleared")

    close_connection(connection, cursor)