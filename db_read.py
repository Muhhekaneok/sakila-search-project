from connection_and_close import make_connection, close_connection
from config_db_read import dbconfig_read


def get_films_by_year(year: int, limit: int = None):
    connection, cursor = make_connection(dbconfig=dbconfig_read)
    if not connection:
        return []

    if limit is None or limit <= 0:
        query = """
            SELECT
                title, release_year
            FROM film
            WHERE release_year = %s;
        """
        cursor.execute(query, (year,))
    else:
        query = """
            SELECT
                title, release_year
            FROM film
            WHERE release_year = %s
            LIMIT %s;
            """
        cursor.execute(query, (year, limit))

    results = cursor.fetchall()
    close_connection(connection, cursor)
    return results


def get_films_by_genre(genre: str, limit: int = None):
    connection, cursor = make_connection(dbconfig=dbconfig_read)
    if not connection:
        return []

    if limit is None or limit <= 0:
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
    else:
        query = """
            SELECT
                f.title, c.name AS genre, f.release_year
            FROM film AS f 
            JOIN film_category AS fc
            ON f.film_id = fc.film_id
            JOIN category AS c
            ON fc.category_id = c.category_id
            WHERE name = %s
            LIMIT %s;
        """
        cursor.execute(query, (genre, limit))

    results = cursor.fetchall()
    close_connection(connection, cursor)
    return results


def get_films_by_year_and_genre(year: int, genre: str, limit: int = None):
    connection, cursor = make_connection(dbconfig=dbconfig_read)
    if not connection:
        return []

    if limit is None or limit <= 0:
        query = """
            SELECT
                f.title, c.name AS genre, f.release_year
            FROM film AS f
            JOIN film_category AS fc
            ON f.film_id = fc.film_id
            JOIN category AS c
            ON c.category_id = fc.category_id
            WHERE f.release_year = %s AND c.name = %s;
        """
        cursor.execute(query, (year, genre))
    else:
        query = """
            SELECT
                f.title, c.name AS genre, f.release_year
            FROM film AS f
            JOIN film_category AS fc
            ON f.film_id = fc.film_id
            JOIN category AS c
            ON c.category_id = fc.category_id
            WHERE f.release_year = %s AND c.name = %s
            LIMIT %s;
        """
        cursor.execute(query, (year, genre, limit))

    result = cursor.fetchall()
    close_connection(connection, cursor)
    return result


def get_actor_by_film_title(title: str):
    connection, cursor = make_connection(dbconfig=dbconfig_read)
    if not connection:
        return []

    query = """
        SELECT
            a.first_name, a.last_name, f.title
        FROM actor AS a
        JOIN film_actor AS fa
        ON a.actor_id = fa.actor_id
        JOIN film as f
        ON fa.film_id = f.film_id
        WHERE f.title = %s;
    """
    cursor.execute(query, (title,))

    result = cursor.fetchall()
    close_connection(connection, cursor)
    return result


def get_customers_info(country: str, limit: int = None):
    connection, cursor = make_connection(dbconfig=dbconfig_read)
    if not connection:
        return []

    if limit is None or limit <= 0:
        query = """
            SELECT
                ci.city,
                co.country,
                a.district,
                a.address,
                cus.first_name,
                cus.last_name,
                cus.email,
                a.phone
            FROM city AS ci
            JOIN country AS co
            ON ci.country_id = co.country_id
            JOIN address AS a
            ON ci.city_id = a.city_id
            JOIN customer AS cus
            ON a.address_id = cus.address_id
            WHERE co.country = %s;
        """
        cursor.execute(query, (country,))
    else:
        query = """
            SELECT
                ci.city,
                co.country,
                a.district,
                a.address,
                cus.first_name,
                cus.last_name,
                cus.email,
                a.phone
            FROM city AS ci
            JOIN country AS co
            ON ci.country_id = co.country_id
            JOIN address AS a
            ON ci.city_id = a.city_id
            JOIN customer AS cus
            ON a.address_id = cus.address_id
            WHERE co.country = %s
            LIMIT %s;
        """
        cursor.execute(query, (country, limit))

    result = cursor.fetchall()
    close_connection(connection, cursor)
    return result