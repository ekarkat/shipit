""" Forms used """
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from web_flask import bycpt
from flask_login import current_user


class RegisterForm(FlaskForm):
    # Register form class
    full_name = StringField('Full name', validators=[DataRequired(), Length(min=3, max=60)])
    address = StringField('Address', validators=[DataRequired(), Length(min=3, max=124)])
    address = StringField('Address', validators=[DataRequired(), Length(min=3, max=248)])
    phone = StringField('Phone number', validators=[DataRequired(), Length(min=3, max=20)])
    postal_code = StringField('Postal code', validators=[DataRequired(), Length(min=3, max=20)])
    birth_date = DateField('Date of Birth')
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=3, max=60)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), Length(min=6), EqualTo('password')])
    submit = SubmitField('Register')

    # costum validation
    def validate_email(self, email):
        from models import storage
        user = storage.user_by_email(email.data)
        if user:
            raise ValidationError("Email already exist")


class LoginForm(FlaskForm):
    # Login form class
    email = StringField('Email', validators=[DataRequired(), Email()])  # Correct function name
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    rememberme = BooleanField('Remember me')
    submit = SubmitField('Log in')

    def validate_email(self, email):
        from models import storage
        user = storage.user_by_email(email.data)
        if not user:
            raise ValidationError("Email doesn't exist")
        
    def validate_password(form, password):
        from models import storage
        user = storage.user_by_email(form.email.data)
        if user:
            passw = user.user_password
            if not bycpt.check_password_hash(user.user_password, password.data):
                raise ValidationError('Wrong password')


class CreateParcel(FlaskForm):
    # Create a parcel form:
    to_name = StringField('Reciver name', validators=[DataRequired()])
    to_phone_number = StringField('Reciver phone number', validators=[DataRequired()])
    to_address = StringField('Reciver address', validators=[DataRequired()])
    # to_city = StringField('Reciver city', validators=[DataRequired()])
    parcel_weight = StringField('parcel weight')
    parcel_cost = FloatField('parcel weight')
    parcel_comments = StringField('comments')
    to_postalcode = StringField('Postal code', validators=[DataRequired(), Length(min=5, max=20)])
    submit = SubmitField('Create')


class UserProfile(FlaskForm):
    # Create a parcel form:
    full_name = StringField('Full name')
    # city = StringField('City', validators=[DataRequired(), Length(min=3, max=20)])
    address = StringField('Address', validators=[DataRequired(), Length(min=3, max=124)])
    phone = StringField('Phone number', validators=[DataRequired(), Length(min=3, max=20)])
    postal_code = StringField('Postal code', validators=[])
    birth_date = DateField('Date of Birth')
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    # costum validation
    def validate_email(self, email):
        from models import storage
        user = storage.user_by_email(email.data)
        if user and user.user_email != current_user.user_email:
            raise ValidationError("Email already exist")

class ContactUs(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=3, max=1024)])
    submit = SubmitField('Send email')


# agent forms agent login and other forms

class AgentLogin(FlaskForm):
    # Agent Login form class
    email = StringField('Email', validators=[DataRequired(), Email()])  # Correct function name
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    rememberme = BooleanField('Remember me')
    submit = SubmitField('Log in')

    def validate_email(self, email):
        from models import storage
        agent = storage.agent_eamil(email.data)
        if not agent:
            raise ValidationError("Email doesn't exist")
        
    # def validate_password(form, password):
    #     from models import storage
    #     agent = storage.agent_eamil(form.email.data)
    #     if agent:
    #         passw = agent.agent_password
    #         if not bycpt.check_password_hash(agent.user_password, password.data):
    #             raise ValidationError('Wrong password')


class PickUp(FlaskForm):
    # Pick up form class
    tracking_number = StringField('Tracking Number', validators=[DataRequired(), Length(min=10)])  # Correct function name
    submit = SubmitField('Submit')

    def validate_tracking_number(self, tracking_number):
        from models import storage
        parcel = storage.parcel_track(tracking_number.data)
        if not parcel:
            raise ValidationError("Tracking number doessn't exist")

    # def validate_password(form, password):
    #     from models import storage
    #     agent = storage.agent_eamil(form.email.data)
    #     if agent:
    #         passw = agent.agent_password
    #         if not bycpt.check_password_hash(agent.user_password, password.data):
    #             raise ValidationError('Wrong password')
class RequestResetForm(FlaskForm):
    # Request reset password class
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


    def validate_email(self, email):
        from models import storage
        user = storage.user_by_email(email.data)
        if user is None:
            raise ValidationError("This account does not exist. You must register first")

class RequestPasswordForm(FlaskForm):
    # Reset password form
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), Length(min=6), EqualTo('password')])
    submit = SubmitField('Reset Password')
