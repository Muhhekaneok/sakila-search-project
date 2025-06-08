from connection_and_close import make_connection, close_connection
from config_db_insert import dbconfig_insert


def create_search_logs_table():
    connection, cursor = make_connection(dbconfig=dbconfig_insert)
    if not connection:
        return

    create_query = """
    CREATE TABLE IF NOT EXISTS search_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        search_type VARCHAR(50),
        search_value VARCHAR(255),
        search_time DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """

    cursor.execute(create_query)
    connection.commit()
    close_connection(connection, cursor)


if __name__ == "__main__":
    create_search_logs_table()
