import os
import sqlite3

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, session, url_for

from forms import LoginForm, RegisterForm, TransactionForm, graphForm
from graphing import generate_graphs

load_dotenv()

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.secret_key = os.getenv("SECRET_KEY")
DATABASE = "finance_project.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            userId INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transactionId INTEGER PRIMARY KEY AUTOINCREMENT,
            transactionDate TEXT NOT NULL,
            transactionTotal DECIMAL NOT NULL,
            transactionItems INTEGER NOT NULL,
            transactionTaxes DECIMAL NOT NULL,
            transactionCategory TEXT NOT NULL,
            transactionPayment TEXT NOT NULL,
            FOREIGN KEY (transactionId) REFERENCES users (userId)
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def home():
    if "username" in session:
        userId = session["userId"]
        username = session["username"]

        graph_html = None

        # show total transactions made up to date
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(
            "SELECT COUNT(*) FROM transactions WHERE transactionId = ?", (userId,)
        )
        total_transactions = c.fetchone()[0]
        conn.close()

        # show all transactions
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM transactions WHERE transactionId = ?", (userId,))
        all_transactions = c.fetchall()
        conn.close()

        form = graphForm()

        if form.validate_on_submit():
            flash("Form successfully submitted", "success")
            print("Form successfully submitted")

            charts = form.graphs.data
            graph_html = generate_graphs(all_transactions, charts)

        return render_template(
            "home.html",
            username=username,
            total_transactions=total_transactions,
            all_transactions=all_transactions,
            graph_form=form,
            graphs=graph_html,
        )

    return redirect(url_for("login"))


@app.route("/about")
def about():
    if "username" in session:
        return render_template("about.html")
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("userId", None)
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Form successfully submitted", "success")
        print("Form successfully submitted")
        username = form.username.data
        password = form.password.data
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(
            "SELECT userId, username FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        user = c.fetchone()
        conn.close()
        if user:
            session["userId"] = user[0]  # Store userId in session
            session["username"] = user[1]  # Store username in session
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password. Please try again.", "error")
            print("Invalid username or password. Please try again.")

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash("Form successfully submitted", "success")
        print("Form successfully submitted")
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = c.fetchone()
        if existing_user:
            flash("Username already exists. Please choose a different one.", "error")
            print("Username already exists. Please choose a different one.")
        else:
            c.execute(
                "INSERT INTO users (name, username, email, password) VALUES (?, ?, ?, ?)",
                (name, username, email, password),
            )
            conn.commit()
            conn.close()
            flash("Registration successful! Please log in.", "success")
            print("Registration successful! Please log in.")
            redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/transaction_log", methods=["GET", "POST"])
def transaction_log():
    if "username" in session:
        form = TransactionForm()
        print("form created", "\n\n\n")
        if form.validate_on_submit():
            flash("Form successfully submitted", "success")
            print("Form successfully submitted")
            transactionId = session["userId"]
            transactionDate = form.transactionDate.data
            transactionTotal = form.transactionTotal.data
            transactionItems = form.transactionItems.data
            transactionTaxes = form.transactionTaxes.data
            transactionCategory = form.transactionCategory.data
            transactionPayment = form.transactionPayment.data
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute(
                "INSERT INTO transactions (transactionId, transactionDate, transactionTotal, transactionItems, transactionTaxes, transactionCategory, transactionPayment) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    transactionId,
                    transactionDate,
                    float(transactionTotal),
                    transactionItems,
                    float(transactionTaxes),
                    transactionCategory,
                    transactionPayment,
                ),
            )
            conn.commit()
            conn.close()
            flash("Transaction logged successfully!", "success")
            return redirect(url_for("home"))
        return render_template("transaction_log.html", form=form)
    else:
        return redirect(url_for("login"))
