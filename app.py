import os
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, session, url_for
import markdown
from supabase import create_client, Client
from smartAI import create_llm, invoke_llm
from forms import LoginForm, RegisterForm, TransactionForm
from graphing import generate_graphs
from extract_data import extract_data
from functools import wraps
import hashlib

# Load environment variables first
load_dotenv()

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.secret_key = os.getenv("SECRET_KEY")

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Global LLM instance for reuse
llm = None
ten_points = None

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# Hash password function
def hash_password(password):
    """Hash a password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

@app.before_request
def before_request():
    """Initialize global LLM instance when needed"""
    global llm
    global supabase
    global ten_points

@app.route("/")
@app.route("/home")
@login_required
def home():
    """
    Renders the home page for logged-in users.
    
    - Fetches and displays the user's transaction history.
    - Generates and embeds graphs based on transaction data.
    - Redirects to the login page if the user is not authenticated.
    
    Returns:
        Rendered template for the home page if authenticated, otherwise a redirect to login.
    """
    response = supabase.table("transactions").select(
        "*", count="exact").eq("userId", session["userId"]).execute()
    total_transactions = response.count

    # Get transactions if not in session
    if "all_transactions" not in session:
        response = supabase.table("transactions").select(
            "*").eq("userId", session["userId"]).execute()
        session['all_transactions'] = response.data
    
    # Process data for display
    df = extract_data(session['all_transactions'])
    graph_html = generate_graphs(session['all_transactions'])

    return render_template(
        "home.html",
        username=session["username"],
        total_transactions=total_transactions,
        df=df,
        graphs=graph_html,
    )

@app.route("/about")
@login_required
def about():
    """
    Renders the About page by reading content from README.md.
    
    - Converts Markdown content to HTML.
    - Redirects to login if the user is not authenticated.
    
    Returns:
        Rendered About page template if authenticated, otherwise a redirect to login.
    """
    try:
        with open("README.md", "r") as f:
            markdown_content = f.read()
        html_content = markdown.markdown(markdown_content)
        return render_template("about.html", about_content=html_content)
    except FileNotFoundError:
        return render_template("about.html", about_content="About page content not found.")

@app.route("/logout")
def logout():
    """Logs out the user by clearing session data."""
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles user authentication.
    
    - Validates login credentials against the database.
    - Initializes a session upon successful login.
    - Redirects to the home page if authentication succeeds.
    """
    if "username" in session:
        return redirect(url_for("home"))
        
    form = LoginForm()
    global supabase
    
    if form.validate_on_submit():
        username = form.username.data
        password = hash_password(form.password.data)

        # Query Supabase for user credentials
        response = supabase.table("users").select("userId, username").eq(
            "username", username).eq("password", password).execute()

        if response.data and len(response.data) > 0:
            user = response.data[0]
            session["userId"] = user["userId"]
            session["username"] = user["username"]
            
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password. Please try again.", "error")

    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Handles user registration.
    
    - Validates form data and checks if the username already exists.
    - Inserts a new user into the database if the username is available.
    - Redirects to the login page upon successful registration.
    """
    
    if "username" in session:
        return redirect(url_for("home"))
        
    form = RegisterForm()
    if form.validate_on_submit():
        flash("Form successfully submitted", "success")
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = hash_password(form.password.data)  # Hash password before storing

        # Check if username exists
        response = supabase.table("users").select(
            "*").eq("username", username).execute()

        if response.data and len(response.data) > 0:
            flash("Username already exists. Please choose a different one.", "error")
        else:
            # Insert new user
            new_user = {
                "name": name,
                "username": username,
                "email": email,
                "password": password
            }
            supabase.table("users").insert(new_user).execute()

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))

    return render_template("register.html", form=form)

@app.route("/transaction_log", methods=["GET", "POST"])
@login_required
def transaction_log():
    """
    Logs a financial transaction for the logged-in user.

    - Displays and validates the transaction form.
    - Extracts and formats transaction details.
    - Stores the transaction in Supabase.
    - Provides user feedback via flash messages.
    - Redirects to home on success or login if not authenticated.
    """
    
    form = TransactionForm()
    if form.validate_on_submit():
        # Format transaction data
        transaction_date = form.transactionDate.data
        if hasattr(transaction_date, 'isoformat'):
            transaction_date = transaction_date.isoformat()

        new_transaction = {
            "userId": session["userId"],
            "transactionDate": transaction_date,
            "transactionSubtotal": float(form.transactionSubtotal.data),
            "transactionItems": form.transactionItems.data,
            "transactionTaxes": float(form.transactionTaxes.data),
            "transactionTotal": float(form.transactionTotal.data),
            "transactionCategory": form.transactionCategory.data,
            "transactionPayment": form.transactionPayment.data
        }

        # Save transaction
        global supabase
        supabase.table("transactions").insert(new_transaction).execute()
        
        # Update transactions in session
        response = supabase.table("transactions").select(
            "*").eq("userId", session["userId"]).execute()
        session['all_transactions'] = response.data

        flash("Transaction logged successfully!", "success")
        return redirect(url_for("home"))
        
    return render_template("transaction_log.html", form=form)

@app.route('/smartspending')
@login_required
def smartspending():
    """
    Generates financial recommendations based on the user's transaction history.

    - Verifies if the user is authenticated via session.
    - If authenticated, analyzes the user's transaction data using an AI model.
    - Uses the `invoke_llm` function to generate financial insights or recommendations.
    - Renders a template displaying the generated insights (`ten_points`).
    - Redirects to the login page if the user is not authenticated.
    """
    global llm
    global ten_points
    if llm is None:
        llm = create_llm()
    if ten_points is None:
        ten_points = invoke_llm(data=session['all_transactions'], llm=llm)
        
    return render_template("smartspending.html", ten_points=ten_points)

if __name__ == "__main__":
    app.run(debug=True)