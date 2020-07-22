from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, Email, Optional, URL


# validators
required = InputRequired()
email_validator = Email(message='Please provide a valid email address')
url_validator = URL(message='Please provide valid URL')
optional = Optional(strip_whitespace=True)
min_4 = Length(min=4)
max_30 = Length(max=30)
max_50 = Length(max=50)


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
        required, min_4, max_30
        ])

    password = PasswordField("Password", validators=[
        required, min_4, max_50
        ])

    remember = BooleanField('Remember me')


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[
        required, min_4, max_30
        ])
    
    email = StringField("Email", validators=[
        required, email_validator
        ])

    profile_image = StringField('Profile Photo', validators=[
                                optional, url_validator
                                ])

    backdrop_image = StringField('Profile Photo', validators=[
                                optional, url_validator
                                ])

    password = PasswordField("Password", validators=[
        required, min_4, max_50
        ])
