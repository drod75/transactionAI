import os
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, session, url_for
import markdown
from supabase import create_client, Client
from smartAI import create_llm, invoke_llm
from forms import LoginForm, RegisterForm, TransactionForm
from graphing import generate_graphs

# Load environment variables first
load_dotenv()

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.secret_key = os.getenv("SECRET_KEY")

# Supabase setup - moved after load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def home():
    if "username" in session:
        userId = session["userId"]
        username = session["username"]

        # Show total transactions made up to date for this user
        response = supabase.table("transactions").select(
            "*", count="exact").eq("userId", userId).execute()
        total_transactions = response.count

        # Show all transactions
        response = supabase.table("transactions").select(
            "*").eq("userId", userId).execute()
        all_transactions = response.data

        session['all_transactions'] = all_transactions

        # Convert Supabase dict format to format expected by generate_graphs
        formatted_transactions = []
        for transaction in all_transactions:
            # Adapt this based on your graphing.py implementation
            formatted_transactions.append(transaction)

        graph_html = generate_graphs(formatted_transactions)

        return render_template(
            "home.html",
            username=username,
            total_transactions=total_transactions,
            all_transactions=all_transactions,
            graphs=graph_html,
        )

    return redirect(url_for("login"))


@app.route("/about")
def about():
    if "username" in session:
        try:
            with open("README.md", "r") as f:
                markdown_content = f.read()
            html_content = markdown.markdown(markdown_content)
            return render_template("about.html", about_content=html_content)
        except FileNotFoundError:
            return render_template("about.html", about_content="About page content not found.")
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("userId", None)
    session.pop("username", None)
    session.pop('all_transactions', None)
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Form successfully submitted", "success")
        username = form.username.data
        password = form.password.data

        # Query Supabase for user credentials
        response = supabase.table("users").select("userId, username").eq(
            "username", username).eq("password", password).execute()

        if response.data and len(response.data) > 0:
            user = response.data[0]
            session["userId"] = user["userId"]
            session["username"] = user["username"]
            
            # llm 
            llm = create_llm()
            session['llm'] = llm
            
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password. Please try again.", "error")

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash("Form successfully submitted", "success")
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data

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
            response = supabase.table("users").insert(new_user).execute()

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/transaction_log", methods=["GET", "POST"])
def transaction_log():
    if "username" in session:
        form = TransactionForm()
        if form.validate_on_submit():
            flash("Form successfully submitted", "success")
            userId = session["userId"]

            transactionDate = form.transactionDate.data
            if hasattr(transactionDate, 'isoformat'):  # Check if it's a date object
                transactionDate = transactionDate.isoformat()

            transactionSubtotal = float(form.transactionSubtotal.data)
            transactionItems = form.transactionItems.data
            transactionTaxes = float(form.transactionTaxes.data)
            transactionCategory = form.transactionCategory.data
            transactionPayment = form.transactionPayment.data

            new_transaction = {
                "userId": userId,
                "transactionDate": transactionDate,
                "transactionSubtotal": transactionSubtotal,
                "transactionItems": transactionItems,
                "transactionTaxes": transactionTaxes,
                "transactionCategory": transactionCategory,
                "transactionPayment": transactionPayment
            }

            response = supabase.table("transactions").insert(
                new_transaction).execute()

            flash("Transaction logged successfully!", "success")
            return redirect(url_for("home"))
        return render_template("transaction_log.html", form=form)
    else:
        return redirect(url_for("login"))


@app.route('/smartspending', methods=['GET', 'POST'])
def smartspending():
    if "username" in session:
        ten_points = invoke_llm(session['all_transactions'], session['llm'])
        return render_template("smartspending.html", ten_points=ten_points)
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
