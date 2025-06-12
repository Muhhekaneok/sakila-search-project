from datetime import datetime

from db_insert import get_clear_table
from db_insert import log_search
from db_read import (get_films_by_year, get_films_by_genre, get_actor_by_film_title, get_customers_info,
                     get_top_n_customers_by_total_spent,
                     get_top_n_customers_by_purchase_count,
                     get_top_customers_last_month_by_total_spent)

from utils import get_limit


def clear_table():
    confirm = input("Are you sure want to clear all logs? (yes/no) ")
    if confirm == "yes".lower():
        get_clear_table()
    else:
        print("clear cancelled")


def handle_search_by_year():
    try:
        year_from = int(input("Enter start year release year since 1990: ").strip())
    except ValueError:
        print("Incorrect start year value")
        return

    to_input = input("Enter end year of release year period or "
                     "leave blank to search only by start year: ").strip()

    try:
        year_to = int(to_input) if to_input else None
    except ValueError:
        print("Incorrect end year value")
        return

    if not (1990 <= year_from <= datetime.max.year):
        print("Start year is out of valid range")
        return

    if year_to is not None and not (year_from <= year_to <= datetime.max.year):
        print("End year must be >= start year and valid")
        return

    limit = get_limit()
    films = get_films_by_year(year_from, year_to, limit)

    if films:
        for row in films:
            title = str(row[0]).ljust(30)
            release_year = str(row[1]).ljust(12)
            print(f"{title} | {release_year}")
        if year_to:
            log_search(search_type="year search", search_value=f"{year_from}-{year_to}")
        else:
            log_search(search_type="year search", search_value=f"{year_from}")
    else:
        print("No film found for the given year(s)")


def handle_search_by_genre():
    genre = input("Enter film genre: ").strip().capitalize()
    limit = get_limit()

    films = get_films_by_genre(genre, limit)

    if films:
        for row in films:
            print(" | ".join(str(col).ljust(30) for col in row))
        log_search(search_type="genre", search_value=genre)
    else:
        print("No film found for this genre")


def handle_search_by_year_and_genre():
    try:
        year = int(input("Enter film release year since 1990: ").strip())
    except ValueError:
        print("Incorrect year value")
        return

    genre = input("Enter film genre: ").strip().capitalize()

    if not (1990 <= year <= datetime.max.year):
        print("Year is out of valid range")
        return

    limit = get_limit()
    films = get_films_by_genre(genre, limit)

    if films:
        for row in films:
            print(" | ".join(str(col).ljust(30) for col in row))
        log_search(search_type="year and genre", search_value=f"{year}, {genre}")
    else:
        print("No films found in this combination")


def handle_search_actor_by_film():
    film = input("Enter film title: ").strip().upper()
    actors = get_actor_by_film_title(film)

    if actors:
        for row in actors:
            print(" | ".join(str(col).ljust(30) for col in row))
        log_search(search_type="actors", search_value=film)
    else:
        print("No actors found for this film")


def handle_search_customers_info_by_countries():
    country = input("Enter country: ").strip().capitalize()
    limit = get_limit()

    customers = get_customers_info(country, limit)

    if customers:
        for row in customers:
            print(" | ".join(str(col).ljust(30) for col in row))
        log_search(search_type="customer info by country", search_value=f"{country}")
    else:
        print("No customers found for this country")


def handle_search_top_n_customers_by_total_spent():
    limit = get_limit()
    top_customers = get_top_n_customers_by_total_spent(limit)

    for row in top_customers:
        print(" | ".join(str(col).ljust(30) for col in row))
    log_search(search_type="top total spent", search_value=f"limit={limit}")


def handle_search_top_n_customers_by_purchase_count():
    limit = get_limit()
    top_customers = get_top_n_customers_by_purchase_count(limit)

    for row in top_customers:
        print(" | ".join(str(col).ljust(30) for col in row))
    log_search(search_type="top purchase count", search_value=f"limit={limit}")


def handle_search_top_n_customers_last_month_by_total_spent():
    year_month = input("Enter year and month (e.g. 2005-06): ").strip()
    limit = get_limit()
    top_customers = get_top_customers_last_month_by_total_spent(year_month, limit)

    if top_customers:
        for row in top_customers:
            print(" | ".join(str(col).ljust(40) for col in row))
        log_search(search_type="top by last month", search_value=f"limit={limit}")
    else:
        print("No payments found for this period")