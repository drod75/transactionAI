import plotly.express as px
from plotly.offline import plot
from datetime import datetime
import pandas as pd

def generate_graphs(all_transactions):
    """
    Generates various interactive graphs to visualize transaction data.

    This function takes a list of transaction data, processes it into a DataFrame, 
    and then creates several types of visualizations: pie charts, bar charts, 
    and line charts, grouped by category, payment method, month, and year.

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
    
    date = [t.get('transactionDate') for t in all_transactions]
    total_cost = [float(t.get('transactionSubtotal', 0)) for t in all_transactions]
    total_items = [int(t.get('transactionItems', 0)) for t in all_transactions]
    total_taxes = [float(t.get('transactionTaxes', 0)) for t in all_transactions]
    categories = [str(t.get('transactionCategory', 'Not Available')) for t in all_transactions]
    cash_or_credit = [str(t.get('transactionPayment', 'Not Available')) for t in all_transactions]
   
    # Create DataFrame
    df = pd.DataFrame({
        'date': date, 
        'total_cost': total_cost, 
        'total_items': total_items, 
        'total_taxes': total_taxes, 
        'categories': categories, 
        'cash_or_credit': cash_or_credit
    })
    
    # Convert date string to datetime
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
   
    # Create aggregations
    cash_or_credit_groupby = df.groupby('cash_or_credit', as_index=False)['cash_or_credit'].count()
    category_df = df.groupby('categories', as_index=False)[['total_cost', 'total_taxes']].mean()
    month_df = df.groupby('month', as_index=False)[['total_cost', 'total_taxes']].mean()
    year_df = df.groupby('year', as_index=False)[['total_cost', 'total_taxes']].mean()
   
    # Generate charts
    graphs = []
    
    category_chart = px.pie(
        df,
        values='total_cost',
        names='categories',
        title='Category Spending Pie',
    )
           
    taxes_chart = px.pie(
        df,
        values='total_taxes',
        names='categories',
        title='Tax per Category Pie',
    )
    
    cash_or_credit_chart = px.bar(
        cash_or_credit_groupby,
        x='cash_or_credit',
        y='cash_or_credit',
        title='Cash or Credit Bar',
    )
   
    category_average_chart = px.bar(
        category_df,
        x='categories',
        y='total_cost',
        title='Category Spending Average Bar',
    )
   
    category_average_taxes = px.bar(
        category_df,
        x='categories',
        y='total_taxes',
        title='Category Taxes Average Bar',
    )
   
    monthly_average_line_chart = px.line(
        month_df,
        x='month',
        y='total_cost',
        title='Monthly Spending Average Line',
    )
   
    monthly_average_taxes_line_chart = px.line(
        month_df,
        x='month',
        y='total_taxes',
        title='Monthly Taxes Average Line',
    )
   
    yearly_average_line_chart = px.line(
        year_df,
        x='year',
        y='total_cost',
        title='Yearly Spending Average Line',
    )
   
    yearly_average_taxes_line_chart = px.line(
        year_df,
        x='year',
        y='total_taxes',
        title='Yearly Taxes Average Line',
    )
   
    # Add all charts to the graphs list
    graphs.append(plot(category_chart, output_type="div"))
    graphs.append(plot(taxes_chart, output_type="div"))
    graphs.append(plot(cash_or_credit_chart, output_type="div"))
    graphs.append(plot(category_average_chart, output_type="div"))
    graphs.append(plot(category_average_taxes, output_type="div"))
    graphs.append(plot(monthly_average_line_chart, output_type="div"))
    graphs.append(plot(monthly_average_taxes_line_chart, output_type="div"))
    graphs.append(plot(yearly_average_line_chart, output_type="div"))
    graphs.append(plot(yearly_average_taxes_line_chart, output_type="div"))
       
    return graphs
