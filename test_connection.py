from config_db_read import dbconfig_read
from connection_and_close import make_connection, close_connection

connection, cursor = make_connection(dbconfig_read)
if connection:
    cursor.execute("select * from actor limit 5")
    result = cursor.fetchall()
    for row in result:
        print(row)

    close_connection(connection, cursor)