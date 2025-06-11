import plotly.express as px
import pandas as pd
from db_read import get_top_customers_last_month_by_total_spent
from utils import get_limit


def plot_top_customers_by_month_px():
    years_months = input("Enter year and month (e.g. 2005-01): ").strip()
    limit = get_limit()

    data = get_top_customers_last_month_by_total_spent(years_months, limit)

    if not data:
        print("No data found for this period")
        return

    df = pd.DataFrame(
        data=data,
        columns=["First Name", "Last Name", "Total"]
    )
    df["Customer"] = df["First Name"] + " " + df["Last Name"]

    fig = px.bar(
        df,
        x="Customer",
        y="Total",
        text="Total",
        labels={"Total": "Total Spent ($)", "Customer": "Customer"},
        title=f"Top Customers in {years_months} by Total Amount"
    )

    fig.update_traces(texttemplate='%{text:.2f}', textposition="outside")
    fig.update_layout(xaxis_tickangle=-45)

    fig.show()