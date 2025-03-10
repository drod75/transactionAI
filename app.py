from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from forms import LoginForm, RegisterForm, TransactionForm
from datetime import datetime
import sqlite3
import os

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
DATABASE = 'finance_project.db'

@app.route('/')
@app.route('/home')
def home():
    pass

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            userId INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transactionID INTEGER PRIMARY KEY AUTOINCREMENT,
            FOREIGN KEY (username) REFERENCES users (username),
            transactionDate TEXT NOT NULL,
            transactionTotal DECIMAL NOT NULL,
            transactionItems INTEGER NOT NULL,
            transactionTaxes DECIMAL NOT NULL,
            transactionsCategory TEXT NOT NULL,
            transactionPayment TEXT NOT NULL,
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
@app.route('/home')
def home():
    if 'username' in session:
        user_id = session['user_id']
        username = session['username']
        
        #show total transactions made up to date
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM transactions WHERE username = ?", (username,))
        total_transactions = c.fetchone()[0]
        conn.close()
        
        #show all transactions
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM transactions WHERE username = ?", (username,))
        all_transactions = c.fetchall()
        conn.close()
        
        return render_template('home.html', username=username, total_transactions=total_transactions, all_transactions=all_transactions)
        
    return redirect(url_for('login'))


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.is_submitted():
        flash("Form successfully submitted")
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['user_id'] = user[0]  # Store user_id in session
            session['username'] = user[1]  # Store username in session
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
        
    return render_template('login.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.is_submitted():
        flash("Form successfully submitted")
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = c.fetchone()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
        else:
            c.execute("INSERT INTO users (username, email, phone, password) VALUES (?, ?, ?, ?)",
                      (username, email, name, password))
            conn.commit()
            conn.close()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login')
    return render_template('register.html')

@app.route('/transaction_log', methods=["GET", "POST"])
def transaction_log():
    if 'username' in session:
        form = TransactionForm()
        if form.is_submitted():
            flash("Form successfully submitted")
        if form.validate_on_submit():
            username = session['username']
            transactionDate = form.transactionDate.data
            transactionTotal = form.transactionTotal.data
            transactionItems = form.transactionItems.data
            transactionTaxes = form.transactionTaxes.data
            transactionCategory = form.transactionCategory.data
            transactionPayment = form.transactionPayment.data
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("INSERT INTO transactions (username, transactionDate, transactionTotal, transactionItems, transactionTaxes, transactionCategory, transactionPayment) VALUES (?, ?, ?, ?, ?, ?)",
                      (username, transactionDate, transactionTotal, transactionItems, transactionTaxes, transactionCategory, transactionPayment))
            conn.commit()
            conn.close()
            flash('Transaction logged successfully!', 'success')
        redirect(url_for('home'))
    else:
        return redirect(url_for('login'))
    
@app.route('/transaction_graphing', methods=["GET", "POST"])
def transaction_graphing():
    if 'username' in session:
        username = session['username']
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT transactionDate, transactionItems, transactionTaxes, transactionsCategory,transactionPayment FROM transactions WHERE username = ?", (username,))
        user_transactions = c.fetchall()
        conn.commit()
        conn.close()
        
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT transactionDate, transactionItems, transactionTaxes, transactionsCategory,transactionPayment FROM transactions")
        global_transactions = c.fetchall()
        return render_template('transaction_graphing.html', user_transactions=user_transactions, global_transactions=global_transactions)
    else:
        return redirect(url_for('login'))