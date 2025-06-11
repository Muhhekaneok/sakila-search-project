import matplotlib.pyplot as plt
from db_read import get_top_customers_last_month_by_total_spent
from utils import get_limit


def plot_top_customers_by_months_plt():
    years_months = input("Enter year and month (e.g. 2005-01): ").strip()
    limit = get_limit()

    data = get_top_customers_last_month_by_total_spent(years_months, limit)

    if not data:
        print("No data found for this period")
        return

    names = [f"{first} {last}" for first, last, _ in data]
    totals = [total for _, _, total in data]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(names, totals)
    plt.title(f"Top Customers in {years_months} by Total Amount")
    plt.xlabel("Customer")
    plt.ylabel("Total Spent ($)")
    plt.xticks(rotation=45, ha="right")

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.2f}",
            ha='center', va='bottom', fontsize=9
        )

    plt.tight_layout()

    plt.show()