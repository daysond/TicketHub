from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length,EqualTo, Email
from wtforms import StringField,PasswordField, SubmitField, ValidationError
from APP.models import User

class PurchaseForm(FlaskForm):
    submit = SubmitField(label="Purchase Ticket")

class RegisterForm(FlaskForm):
    
    def validate_username(self, temp_username):
        user = User.query.filter_by(name=temp_username.data).first()
        if user:
            raise ValidationError('Username already exists!')
    
    def validate_email_address(self, temp_email_address):
        email = User.query.filter_by(email=temp_email_address.data).first()
        if email:
            raise ValidationError('Email address already exists!')
    
    username = StringField('Username:', [Length(min=2, max=30), DataRequired()])
    email_address = StringField('Email Address:', [Email(), DataRequired()])
    password = PasswordField('Password:', [Length(min=6, max=30), DataRequired()])
    confirm = PasswordField('Password Confirm:', [EqualTo("password", message = 'password must match!'), DataRequired()])
    submit = SubmitField('Create Account')

class LoginForm(FlaskForm):
    
    username = StringField('Username:', [DataRequired()])
    password = PasswordField('Password:', [DataRequired()])
    submit = SubmitField('Log in')
    
# class SeatingForm(FlaskForm):
#     # def __init__(self, seatings: list = None, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)
        
