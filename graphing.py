import plotly.express as px
from database import Database

db = Database()

def get_user_data(username: str):
    """
    Retrieves user data from the database given a username.

    Parameters:
        username (str): The username to retrieve data for.

    Returns:
        A dictionary containing the user's data.
    """
    data = db.supabase.table("users").select("user_id").eq("username", username).execute()
    user_transactions = db.supabase.table("transactions").select("*").eq("user_id", data.data[0]["user_id"]).execute()
    return user_transactions

def graph(userdata, graph_types) -> list:
    df = pd.DataFrame(userdata)
    graphs = []
    
    