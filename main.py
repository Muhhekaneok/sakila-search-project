from datetime import datetime

from db_read import get_films_by_year, get_films_by_genre
from db_insert import log_search, get_clear_table


def main():
    choice = input("""
    === Welcome to Sakila Search ===
    
    0 - clear table
    1 - search by year
    2 - search by genre
    """)
    if choice == "0":
        confirm = input("Are you sure want to clear all logs? (yes/no) ")
        if confirm == "yes".lower():
            get_clear_table()
        else:
            print("clear cancelled")

    elif choice == "1":
        try:
            year = int(input("Enter film release year: "))
        except ValueError:
            print("Incorrect year value")
            return

        if 1990 <= year <= datetime.max.year:
            films = get_films_by_year(year)
            if films:
                for title, release_year in films:
                    print(f"Film: {title}, release year: {release_year}")
                log_search("year search", str(year))
            else:
                print("Films not found for this year")
        else:
            print("Year is out of valid range")

    elif choice == "2":
        genre = input("Enter film genre: ").capitalize()

        films = get_films_by_genre(genre)
        print(films)
        if films:
            for row in films:
                title = str(row[0]).ljust(30)
                genre = str(row[1]).ljust(12)
                year = str(row[2]).ljust(2)
                # print("\t | \t".join(str(col) for col in row))
                print(f"{title} | {genre} | {year}")
            log_search("genre search", genre)
        else:
            print(f"Film by genre not found")

    else:
        print("Incorrect choice")


if __name__ == "__main__":
    main()
