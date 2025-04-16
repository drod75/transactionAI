# Importing FlaskForm base class to create web forms
from flask_wtf import FlaskForm

# Importing various field types to use in the forms
from wtforms import (
    DateField,            # For selecting a date (e.g., transaction date)
    DecimalField,         # For decimal numbers (e.g., money values)
    IntegerField,         # For whole numbers (e.g., item counts)
    PasswordField,        # For obscured text input (e.g., login password)
    SelectField,          # For single-choice dropdowns
    SelectMultipleField,  # (Not used here, but allows selecting multiple options)
    StringField,          # For plain text input (e.g., name, email)
    SubmitField,          # Button to submit the form
)

# Validators ensure form fields meet conditions before accepting submission
from wtforms.validators import DataRequired  # Ensures field is not empty

# ----------------------------- #
# 📋 User Registration Form     #
# ----------------------------- #

class RegisterForm(FlaskForm):
    # Text field for the user's full name (required)
    name = StringField("Name", validators=[DataRequired()])
    
    # Text field for email input (required)
    email = StringField("Email", validators=[DataRequired()])
    
    # Text field for username (required)
    username = StringField("Username", validators=[DataRequired()])
    
    # Password field with masking (required)
    password = PasswordField("Password", validators=[DataRequired()])
    
    # Button to submit the form
    submit = SubmitField("Register")


# ----------------------------- #
# 🔐 User Login Form            #
# ----------------------------- #

class LoginForm(FlaskForm):
    # Username field (required)
    username = StringField("Username", validators=[DataRequired()])
    
    # Password field (required)
    password = PasswordField("Password", validators=[DataRequired()])
    
    # You could add CAPTCHA here for security (commented out)
    # recaptcha = RecaptchaField(parameters)
    
    # Submit button
    submit = SubmitField("Login")


# ----------------------------- #
# 💵 Transaction Logging Form   #
# ----------------------------- #

class TransactionForm(FlaskForm):
    # Date input for when the transaction occurred (required)
    transactionDate = DateField("Transaction Date", validators=[DataRequired()])
    
    # Decimal input for the subtotal amount before tax (required)
    transactionSubtotal = DecimalField("Transaction Subtotal", validators=[DataRequired()])
    
    # Dropdown menu to select category of the transaction (required)
    transactionCategory = SelectField(
        "Category",
        [DataRequired()],
        choices=[
            ("Food", "Food"),
            ("Entertainment", "Entertainment"),
            ("Clothing", "Clothing"),
            ("Transportation", "Transportation"),
            ("Utilities", "Utilities"),
            ("Health", "Health"),
            ("Personal", "Personal"),
            ("Gift", "Gift"),
            ("Other", "Other"),
        ],
    )
    
    # Integer input for number of items purchased (required)
    transactionItems = IntegerField("Number of Items", validators=[DataRequired()])
    
    # Decimal input for tax paid (required)
    transactionTaxes = DecimalField("Taxes", validators=[DataRequired()])
    
    # Decimal input for total cost after tax (required)
    transactionTotal = DecimalField("Transaction Total", validators=[DataRequired()])
    
    # Dropdown to choose between cash or credit payment (required)
    transactionPayment = SelectField(
        "Cash or Credit",
        [DataRequired()],
        choices=[("Cash", "Cash"), ("Credit", "Credit")],
    )
    
    # Submit button for logging the transaction
    submit = SubmitField("Log Transaction")
