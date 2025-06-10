from config_db_read import dbconfig_read
from connection_and_close import make_connection, close_connection


def get_films_by_year(year_from: int, year_to: int = None, limit: int = None):
    connection, cursor = make_connection(dbconfig=dbconfig_read)
    if not connection:
        return []

    base_query = """
        SELECT
            title, release_year
        FROM film
        WHERE release_year >= %s
    """

    params = [year_from]

    if year_to is not None:
        base_query += " AND release_year <= %s"
        params.append(year_to)

    base_query += " ORDER BY release_year ASC"

    if limit and limit > 0:
        base_query += " LIMIT %s"
        params.append(limit)

    cursor.execute(base_query, tuple(params))

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


def get_top_n_customers_by_total_spent(limit: int = None):
    connection, cursor = make_connection(dbconfig=dbconfig_read)
    if not connection:
        return []

    if limit is None or limit <= 0:
        query = """
            SELECT
                cus.first_name, cus.last_name, SUM(p.amount) AS total_spent
            FROM customer AS cus
            JOIN payment AS p
            ON cus.customer_id = p.customer_id
            GROUP BY cus.customer_id
            ORDER BY total_spent DESC
        """
        cursor.execute(query)
    else:
        query = """
            SELECT
                cus.first_name, cus.last_name, SUM(p.amount) AS total_spent
            FROM customer AS cus
            JOIN payment AS p
            ON cus.customer_id = p.customer_id
            GROUP BY cus.customer_id
            ORDER BY total_spent DESC
            LIMIT %s;
        """
        cursor.execute(query, (limit,))

    result = cursor.fetchall()
    close_connection(connection, cursor)
    return result


def get_top_n_customers_by_purchase_count(limit: int = None):
    connection, cursor = make_connection(dbconfig=dbconfig_read)
    if not connection:
        return []

    if limit is None or limit <= 0:
        query = """
            SELECT
                cus.first_name, cus.last_name, COUNT(p.payment_id) AS count_payment
            FROM customer AS cus
            JOIN payment AS p
            ON cus.customer_id = p.customer_id
            GROUP BY cus.customer_id
            ORDER BY count_payment DESC;
        """
        cursor.execute(query)
    else:
        query = """
            SELECT
                cus.first_name, cus.last_name, COUNT(p.payment_id) AS count_payment 
            FROM customer AS cus
            JOIN payment AS p
            ON cus.customer_id = p.customer_id
            GROUP BY cus.customer_id
            ORDER BY count_payment DESC
            LIMIT %s;
        """
        cursor.execute(query, (limit,))

    result = cursor.fetchall()
    close_connection(connection, cursor)
    return result


def get_top_customers_last_month_by_total_spent(year_month: str, limit: int = None):
    connection, cursor = make_connection(dbconfig=dbconfig_read)
    if not connection:
        return []

    if limit is None or limit <= 0:
        query = """
            SELECT
                cus.first_name, cus.last_name, SUM(p.amount) AS total_spent
            FROM customer AS cus
            JOIN payment AS p
            ON cus.customer_id = p.customer_id
            WHERE DATE_FORMAT(p.payment_date, "%Y-%m") = %s
            GROUP BY cus.customer_id
            ORDER BY total_spent DESC;
        """
        cursor.execute(query, (year_month,))
    else:
        query = """
            SELECT
                cus.first_name, cus.last_name, SUM(p.amount) AS total_spent
            FROM customer AS cus
            JOIN payment AS p
            ON cus.customer_id = p.customer_id
            WHERE DATE_FORMAT(p.payment_date, "%Y-%m") = %s
            GROUP BY cus.customer_id
            ORDER BY total_spent DESC
            LIMIT %s;
        """
        cursor.execute(query, (year_month, limit))

    result = cursor.fetchall()
    close_connection(connection, cursor)
    return result