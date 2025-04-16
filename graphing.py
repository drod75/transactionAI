import plotly.express as px
from plotly.offline import plot
from datetime import datetime
from extract_data import extract_data
import pandas as pd

def generate_graphs(all_transactions):
    """
    Generates various interactive graphs to visualize transaction data.

    This function takes a list of transaction data, processes it into a DataFrame,
    and then creates several types of visualizations: pie charts and bar charts,
    grouped by category, payment method, weekday, and month.

    Args:
        all_transactions (list): A list of dictionaries, where each dictionary
                                  contains details about a transaction.

    Returns:
        list: A list of Plotly graph HTML div elements containing the generated
              charts, or None if no transactions are provided.
    """
    # Check if there are any transactions
    if not all_transactions:
        return None

    graphs = []
    df = extract_data(all_transactions)

    category_spending = df.groupby('Category')['Total'].sum().reset_index()
    fig_cat_pie = px.pie(category_spending,
                         values='Total',
                         color='Category',
                         names='Category',
                         title='Spending Distribution by Category')
    graphs.append(plot(fig_cat_pie, output_type="div"))


    payment_spending = df.groupby('Payment Method')['Total'].sum().reset_index()
    fig_pay_pie = px.pie(payment_spending,
                         values='Total',
                         color='Payment Method',
                         names='Payment Method',
                         title='Spending Distribution by Payment Method')
    graphs.append(plot(fig_pay_pie, output_type="div"))

    weekday_spending = df.groupby('Weekday')['Total'].mean().reset_index()
    fig_weekday_bar = px.bar(weekday_spending,
                             x='Weekday',
                             y='Total',
                             color="Weekday",
                             title='Day of the Week Average Spending',
                             labels={'Total': 'Total Spending ($)', 'Weekday': 'Day of Week'})
    fig_weekday_bar.update_layout(xaxis_title='Day of Week', yaxis_title='Average Spending ($)')
    graphs.append(plot(fig_weekday_bar, output_type="div"))

    monthly_spending = df.groupby('Month')['Total'].sum().reset_index()
    fig_month_bar = px.bar(monthly_spending,
                           x='Month',
                           y='Total',
                           color="Month",
                           title='Monthly Spending',
                           labels={'Total': 'Total Spending ($)', 'Month': 'Month'})
    fig_month_bar.update_layout(xaxis_title='Month', yaxis_title='Total Spending ($)')
    graphs.append(plot(fig_month_bar, output_type="div"))


    return graphs
