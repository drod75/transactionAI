import pandas as pd

def extract_data(all_transactions) -> pd.DataFrame:
    date = [t.get('transactionDate') for t in all_transactions]
    items = [int(t.get('transactionItems')) for t in all_transactions]
    subtotal = [round(float(t.get('transactionSubtotal')), 2) for t in all_transactions]
    taxes = [round(float(t.get('transactionTaxes')), 2) for t in all_transactions]
    total = [round(float(t.get('transactionTotal')), 2) for t in all_transactions]
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
    df['Datetime'] = df['Date'].dt.strftime('%Y-%m-%d')
    df['Month'] = df['Date'].dt.month_name()
    month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)
    df['Year'] = df['Date'].dt.year
    df['Weekday'] = df['Date'].dt.day_name()
    weekday_order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    df['Weekday'] = pd.Categorical(df['Weekday'], categories=weekday_order, ordered=True)
        
    return df