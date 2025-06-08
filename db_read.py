from connection_and_close import make_connection, close_connection
from config_db_read import dbconfig_read


def get_films_by_year(year: int):
    connection, cursor = make_connection(dbconfig=dbconfig_read)
    if not connection:
        return []

    query = """
    SELECT
        title, release_year
    FROM film
    WHERE release_year = %s;
    """
    cursor.execute(query, (year,))
    results = cursor.fetchall()

    close_connection(connection, cursor)
    return results


def get_films_by_genre(genre: str):
    connection, cursor = make_connection(dbconfig=dbconfig_read)
    if not connection:
        return []

    query = """
    SELECT
        f.title, c.name AS genre, f.release_year
    FROM film AS f 
    JOIN film_category AS fc
    ON f.film_id = fc.film_id
    JOIN category AS c
    ON fc.category_id = c.category_id
    WHERE name = %s;
    """
    cursor.execute(query, (genre,))
    results = cursor.fetchall()

    close_connection(connection, cursor)
    return results