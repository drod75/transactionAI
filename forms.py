from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    DecimalField,
    IntegerField,
    PasswordField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    # recaptcha = RecaptchaField(parameters)
    submit = SubmitField("Login")


class TransactionForm(FlaskForm):
    transactionDate = DateField("Transaction Date", validators=[DataRequired()])
    transactionSubtotal = DecimalField("Transaction Subtotal", validators=[DataRequired()])
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
    transactionItems = IntegerField("Number of Items", validators=[DataRequired()])
    transactionTaxes = DecimalField("Taxes", validators=[DataRequired()])
    transactionTotal = DecimalField("Transaction Total", validators=[DataRequired()])
    transactionPayment = SelectField(
        "Cash or Credit",
        [DataRequired()],
        choices=[("Cash", "Cash"), ("Credit", "Credit")],
    )
    submit = SubmitField("Log Transaction")
