from datetime import datetime

from db_read import (get_films_by_year, get_films_by_genre, get_films_by_year_and_genre,
                     get_actor_by_film_title, get_customers_info)
from db_insert import log_search, get_clear_table
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
                year = int(input("Enter film release year since 1990: "))
            except ValueError:
                print("Incorrect year value")
                return

            if 1990 <= year <= datetime.max.year:
                limit = get_limit()
                films = get_films_by_year(year, limit)
                if films:
                    for row in films:
                        title = str(row[0]).ljust(30)
                        release_year = str(row[1]).ljust(12)
                        print(f"{title} | {release_year}")
                    log_search("year search", str(year))
                else:
                    print("Films not found for this year")
            else:
                print("Year is out of valid range")

        elif choice == "2":
            genre = input("Enter film genre: ").capitalize()
            limit = get_limit()
            films = get_films_by_genre(genre, limit)
            if films:
                for row in films:
                    title = str(row[0]).ljust(30)
                    genre = str(row[1]).ljust(12)
                    year = str(row[2]).ljust(2)
                    print(f"{title} | {genre} | {year}")
                log_search("genre search", genre)
            else:
                print(f"Film by genre not found")

        elif choice == "3":
            try:
                year = int(input("Enter film release year since 1990: "))
            except ValueError:
                print("Incorrect year value")
                return
            genre = input("Enter film genre: ").capitalize()

            if 1990 <= year <= datetime.max.year:
                limit = get_limit()
                films = get_films_by_year_and_genre(year, genre, limit)
                if films:
                    for row in films:
                        title = str(row[0]).ljust(30)
                        genre = str(row[1]).ljust(12)
                        year = str(row[2]).ljust(2)
                        print(f"{title} | {genre} | {year}")
                    log_search(search_type="year and genre search", search_value=f"{year}, {genre}")
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

        elif choice == "q":
            break

        else:
            print("Incorrect choice. Try again")


if __name__ == "__main__":
    main()
