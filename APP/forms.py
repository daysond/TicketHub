from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField, ValidationError

class PurchaseForm(FlaskForm):
    submit = SubmitField(label="Purchase Ticket")