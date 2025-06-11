from datetime import datetime

from db_read import (get_films_by_year, get_films_by_genre, get_films_by_year_and_genre,
                     get_actor_by_film_title, get_customers_info, get_top_n_customers_by_total_spent,
                     get_top_n_customers_by_purchase_count, get_top_customers_last_month_by_total_spent)
from db_insert import log_search, get_clear_table
from plt_top_customers import plot_top_customers_by_months_plt
from plotly_top_customers import plot_top_customers_by_month_px
from utils import get_limit


def main():
    while True:
        choice = input("""
        === Welcome to Sakila Search ===
        
        0 - clear table
        1 - search by year
        2 - search by genre
        3 - search by year and genre
        4 - search actor by film
        5 - search info about customers by countries
        6 - search top N customers by total spent
        7 - search top N customers by purchase count
        8 - search top N customers last month by total spent
        9 - plot top customers by month (matplotlib)
        10 - plot top customers by month (plotly)
        
        q - for exit program
        """)
        if choice == "0":
            confirm = input("Are you sure want to clear all logs? (yes/no) ")
            if confirm == "yes".lower():
                get_clear_table()
            else:
                print("clear cancelled")

        elif choice == "1":
            try:
                year_from = int(input("Enter start year release year since 1990: "))
            except ValueError:
                print("Incorrect year value")
                return

            to_input = input("Enter end of release year "
                             "(or leave blank to search only by start year): ").strip()

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
                print("No films found for the given year(s)")

        elif choice == "2":
            genre = input("Enter film genre: ").capitalize()
            limit = get_limit()
            films = get_films_by_genre(genre, limit)

            if films:
                for row in films:
                    title = str(row[0]).ljust(30)
                    genre = str(row[1]).ljust(12)
                    year_from = str(row[2]).ljust(2)
                    print(f"{title} | {genre} | {year_from}")
                log_search("genre search", genre)
            else:
                print(f"Film by genre not found")

        elif choice == "3":
            try:
                year_from = int(input("Enter film release year since 1990: "))
            except ValueError:
                print("Incorrect year value")
                return
            genre = input("Enter film genre: ").capitalize()

            if 1990 <= year_from <= datetime.max.year:
                limit = get_limit()
                films = get_films_by_year_and_genre(year_from, genre, limit)
                if films:
                    for row in films:
                        title = str(row[0]).ljust(30)
                        genre = str(row[1]).ljust(12)
                        year_from = str(row[2]).ljust(2)
                        print(f"{title} | {genre} | {year_from}")
                    log_search(search_type="year and genre search", search_value=f"{year_from}, {genre}")
                else:
                    print("No films found in this combination")
            else:
                print("Year is out of valid range")

        elif choice == "4":
            film_title = input("Enter film title to find actor info: ").upper()
            actors = get_actor_by_film_title(film_title)

            if actors:
                for row in actors:
                    first = str(row[0]).ljust(8)
                    last = str(row[1]).ljust(9)
                    title = str(row[2]).ljust(15)
                    print(f"{first} | {last} | {title}")
                log_search(search_type="actor info", search_value=film_title)
            else:
                print("No actors found for this film")

        elif choice == "5":
            country_name = input("Enter country to find info about customers from it: ").capitalize()
            limit = get_limit()
            customers = get_customers_info(country_name, limit)

            if customers:
                for row in customers:
                    city = str(row[0]).ljust(25)
                    country = str(row[1]).ljust(25)
                    district = str(row[2]).ljust(25)
                    address = str(row[3]).ljust(40)
                    first_name = str(row[4]).ljust(10)
                    last_name = str(row[5]).ljust(10)
                    email = str(row[6]).ljust(10)
                    phone = str(row[7]).ljust(12)
                    print(f"{city} | {country} | {district} | {address} |"
                          f"{first_name} | {last_name} | {email} | {phone}")
                log_search(search_type="customers info", search_value=f"{country_name}")
            else:
                print("No customers found for this country")

        elif choice == "6":
            limit = get_limit()
            top_customers = get_top_n_customers_by_total_spent(limit)
            for row in top_customers:
                first_name = str(row[0]).ljust(15)
                last_name = str(row[1]).ljust(15)
                total_spent = str(row[2]).ljust(10)
                print(f"{first_name} | {last_name} | {total_spent}")
            log_search(search_type="top total spent", search_value=f"limit={limit}")

        elif choice == "7":
            limit = get_limit()
            top_customers = get_top_n_customers_by_purchase_count(limit)
            for row in top_customers:
                first_name = str(row[0]).ljust(15)
                last_name = str(row[1]).ljust(15)
                purchase_count = str(row[2]).ljust(15)
                print(f"{first_name} | {last_name} | {purchase_count}")
            log_search(search_type="top purchase count", search_value=f"limit={limit}")

        elif choice == "8":
            year_month = input("Enter year and month (e.g. 2006-01): ").strip()
            limit = get_limit()
            top_customers = get_top_customers_last_month_by_total_spent(year_month, limit)

            if top_customers:
                for row in top_customers:
                    first_name = str(row[0]).ljust(15)
                    last_name = str(row[1]).ljust(15)
                    total_spent = str(row[2]).ljust(10)
                    print(f"{first_name} | {last_name} | {total_spent}")
                log_search(search_type="top last month", search_value=f"limit={limit}")
            else:
                print("No payments found for last month")

        elif choice == "9":
            plot_top_customers_by_months_plt()

        elif choice == "10":
            plot_top_customers_by_month_px()

        elif choice == "q":
            break

        else:
            print("Incorrect choice. Try again")


if __name__ == "__main__":
    main()
