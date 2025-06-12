from datetime import datetime

from handlers import (clear_table, handle_search_by_year, handle_search_by_genre, handle_search_by_year_and_genre,
                      handle_search_actor_by_film, handle_search_customers_info_by_countries,
                      handle_search_top_n_customers_by_total_spent,
                      handle_search_top_n_customers_by_purchase_count,
                      handle_search_top_n_customers_last_month_by_total_spent)

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
            clear_table()

        elif choice == "1":
            handle_search_by_year()

        elif choice == "2":
            handle_search_by_genre()

        elif choice == "3":
            handle_search_by_year_and_genre()

        elif choice == "4":
            handle_search_actor_by_film()

        elif choice == "5":
            handle_search_customers_info_by_countries()

        elif choice == "6":
            handle_search_top_n_customers_by_total_spent()

        elif choice == "7":
            handle_search_top_n_customers_by_purchase_count()

        elif choice == "8":
            handle_search_top_n_customers_last_month_by_total_spent()

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
