import os
from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

# Supabase configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL and Key must be set as environment variables.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Helper function to get the current user
def get_current_user():
    if 'user_id' in session:
        return supabase.auth.get_user(session['user_id'])
    return None

# Routes
@app.route('/')
def home():
    user = get_current_user()
    return render_template('home.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            # Sign in user
            result = supabase.auth.sign_in_with_password({"email": email, "password": password})
            session['user_id'] = result.user.id
            session.modified = True
            return redirect(url_for('dashboard'))
        except Exception as e:
            return render_template('login.html', error=str(e))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        try:
            # Check if username already exists
            query = supabase.table("users").select("*").eq("username", username)
            result = query.execute()
            print(f"Result object: {result}")
            if len(result.data) > 0:
                return render_template('register.html', error="Username already exists. Please choose a different username.")

            # Sign up user
            result = supabase.auth.sign_up({"email": email, "password": password})
            session['user_id'] = result.user.id
            session.modified = True

            # Insert user data into the 'users' table
            user_data = {
                "user_id": result.user.id,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "username": username
            }
            data, error = supabase.table("users").insert(user_data).execute()
            if error:
                print(f"Error inserting user data: {error}")
                return render_template('register.html', error="Registration failed. Please try again.")

            return redirect(url_for('dashboard'))
        except Exception as e:
            return render_template('register.html', error=str(e))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))

    try:
        # Fetch last 10 transactions
        query = supabase.table("transactions").select("*").eq("user_id", user.user.id).order("date", desc=True).limit(10)
        last_10_transactions_result, error = query.execute()
        if error:
            print(f"Error fetching last 10 transactions: {error}")
            last_10_transactions = []
        else:
            last_10_transactions = last_10_transactions_result.data

        return render_template('dashboard.html', user=user, last_10_transactions=last_10_transactions)
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return render_template('dashboard.html', user=user, error="Failed to fetch transactions.")

@app.route('/log_transaction', methods=['POST'])
def log_transaction():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))

    date = request.form['date']
    total = float(request.form['total'])
    category = request.form['category']
    items = int(request.form['items'])
    taxes = float(request.form['taxes'])
    payment_method = int(request.form['payment_method'])

    try:
        transaction_data = {
            "user_id": user.user.id,
            "date": date,
            "total": total,
            "category": category,
            "items": items,
            "taxes": taxes,
            "payment_method": payment_method
        }
        data, error = supabase.table("transactions").insert(transaction_data).execute()
        if error:
            print(f"Error logging transaction: {error}")
            return render_template('dashboard.html', user=user, error="Failed to log transaction. Please try again.")

        return redirect(url_for('dashboard'))
    except Exception as e:
        print(f"Error logging transaction: {e}")
        return render_template('dashboard.html', user=user, error="Failed to log transaction. Please try again.")

@app.route('/view_all_transactions')
def view_all_transactions():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))

    try:
        # Fetch all transactions
        query = supabase.table("transactions").select("*").eq("user_id", user.user.id).order("date", desc=True)
        all_transactions_result, error = query.execute()
        if error:
            print(f"Error fetching all transactions: {error}")
            all_transactions = []
        else:
            all_transactions = all_transactions_result.data

        return render_template('all_transactions.html', user=user, all_transactions=all_transactions)
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return render_template('dashboard.html', user=user, error="Failed to fetch transactions.")


@app.route('/account')
def account():
    user = get_current_user()
    return render_template('account.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)