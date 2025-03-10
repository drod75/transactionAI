"""Initialize app."""

from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from forms import LoginForm, RegisterForm, TransactionForm
import os

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

@app.route('/')
@app.route('/home')
def home():
    pass


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pass
    pass

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        pass
    pass

@app.route('/transaction_log', methods=["GET", "POST"])
def transaction_log():
    form = TransactionForm()
    pass