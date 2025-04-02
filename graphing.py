import plotly.express as px
from plotly.offline import plot
from datetime import datetime
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

    # Extract data
    date = [t.get('transactionDate') for t in all_transactions]
    items = [int(t.get('transactionItems')) for t in all_transactions]
    subtotal = [float(t.get('transactionSubtotal')) for t in all_transactions]
    taxes = [float(t.get('transactionTaxes')) for t in all_transactions]
    total = [float(t.get('transactionTotal')) for t in all_transactions] # Using Total as per current file
    categories = [t.get('transactionCategory') for t in all_transactions]
    cash_or_credit = [t.get('transactionPayment') for t in all_transactions]

    df = pd.DataFrame(
        {'Date': date,
         'Items': items,
         'Subtotal': subtotal,
         'Taxes': taxes,
         'Total': total,
         'Category': categories,
         'Payment Method': cash_or_credit
         }
    )

    # Ensure Date is datetime type
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month_name()
    month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)
    df['Year'] = df['Date'].dt.year
    df['Weekday'] = df['Date'].dt.day_name()
    weekday_order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    df['Weekday'] = pd.Categorical(df['Weekday'], categories=weekday_order, ordered=True)

    category_spending = df.groupby('Category')['Total'].sum().reset_index()
    fig_cat_pie = px.pie(category_spending,
                         values='Total',
                         names='Category',
                         title='Spending Distribution by Category')
    graphs.append(plot(fig_cat_pie, output_type="div"))


    payment_spending = df.groupby('Payment Method')['Total'].sum().reset_index()
    fig_pay_pie = px.pie(payment_spending,
                         values='Total',
                         names='Payment Method',
                         title='Spending Distribution by Payment Method')
    graphs.append(plot(fig_pay_pie, output_type="div"))

    weekday_spending = df.groupby('Weekday')['Total'].mean().reset_index()
    fig_weekday_bar = px.bar(weekday_spending,
                             x='Weekday',
                             y='Total',
                             title='Day of the Week Average Spending',
                             labels={'Total': 'Total Spending ($)', 'Weekday': 'Day of Week'})
    fig_weekday_bar.update_layout(xaxis_title='Day of Week', yaxis_title='Average Spending ($)')
    graphs.append(plot(fig_weekday_bar, output_type="div"))

    monthly_spending = df.groupby('Month')['Total'].sum().reset_index()
    fig_month_bar = px.bar(monthly_spending,
                           x='Month',
                           y='Total',
                           title='Monthly Spending',
                           labels={'Total': 'Total Spending ($)', 'Month': 'Month'})
    fig_month_bar.update_layout(xaxis_title='Month', yaxis_title='Total Spending ($)')
    graphs.append(plot(fig_month_bar, output_type="div"))


    return graphs
