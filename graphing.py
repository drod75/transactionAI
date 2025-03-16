import plotly.graph_objects as go
from plotly.offline import plot


def generate_graphs(all_transactions, charts):
    graphs = []
    categories = [t[5] for t in all_transactions]
    totals = [float(t[2]) for t in all_transactions]

    for graph_type in charts:
        if graph_type == "Pie Chart":
            fig = go.Figure(data=[go.Pie(labels=categories, values=totals)])
        elif graph_type == "Bar Chart":
            fig = go.Figure(data=[go.Bar(x=categories, y=totals)])
        elif graph_type == "Line Chart":
            fig = go.Figure(data=[go.Scatter(x=categories, y=totals, mode="lines")])
        elif graph_type == "Scatter Plot":
            fig = go.Figure(data=[go.Scatter(x=categories, y=totals, mode="markers")])
        else:
            continue  # Skip invalid graph types

        graphs.append(plot(fig, output_type="div"))

    return graphs
