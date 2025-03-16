from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DecimalField, SelectField, BooleanField, DateField
from wtforms.validators import DataRequired, Email
from dotenv import load_dotenv
import os

load_dotenv()

# os.environ["RECAPTCHA_PUBLIC_KEY"] = os.getenv("RECAPTCHA_PUBLIC_KEY")
# os.environ["RECAPTCHA_PRIVATE_KEY"] = os.getenv("RECAPTCHA_PRIVATE_KEY")

# parameters = {"RECAPTCHA_PUBLIC_KEY": os.getenv("RECAPTCHA_PUBLIC_KEY"), "RECAPTCHA_PRIVATE_KEY": os.getenv("RECAPTCHA_PRIVATE_KEY")}

class RegisterForm(FlaskForm):
    '''
    Form for users to create new account
    
    Attributes:
        name (StringField): Name of user
        email (StringField): Email of user
        username (StringField): Username of user
        password (PasswordField): Password of user
        submit (SubmitField): Submit button
    '''
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')
    
class LoginForm(FlaskForm):
    '''
    Form for users to login
    
    Attributes:
        username (StringField): Username of user
        password (PasswordField): Password of user
        recaptcha (RecaptchaField): Recaptcha field
        submit (SubmitField): Submit button
    '''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    # recaptcha = RecaptchaField(parameters)
    submit = SubmitField('Login')
    
class TransactionForm(FlaskForm):
    '''
    Form for users to log transactions
    
    Attributes:
        transaction_date (DateField): Date of transaction
        transaction_total (DecimalField): Total of transaction
        transaction_category (SelectField): Category of transaction
        transaction_items (IntegerField): Number of items in transaction
        transaction_taxes (DecimalField): Taxes of transaction
        transaction_cash_or_credit (SelectField): Cash or Credit of transaction
    '''
    
    transactionDate = DateField('Transaction Date', validators=[DataRequired()])
    transactionTotal = DecimalField('Transaction Total', validators=[DataRequired()])
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
            ("Other", "Other")
        ],
    )
    transactionItems = IntegerField('Number of Items', validators=[DataRequired()])
    transactionTaxes = DecimalField('Taxes', validators=[DataRequired()])
    transactionPayment = SelectField(
        "Cash or Credit",
        [DataRequired()],
        choices=[
            ("Cash", "Cash"),
            ("Credit", "Credit")
        ],
    )
    submit = SubmitField('Log Transaction')