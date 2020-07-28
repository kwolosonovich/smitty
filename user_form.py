from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FileField
from wtforms.validators import InputRequired, Email, Length, Optional, URL
from flask_wtf.file import FileField, FileAllowed


# validators
required = InputRequired()
email_validator = Email(message='Please provide a valid email address')
url_validator = URL(message='Please provide valid URL')
optional = Optional(strip_whitespace=True)
min_4 = Length(min=4)
max_50 = Length(max=50)
max_80 = Length(max=80)

# images = UploadSet('images', IMAGES)
file = FileAllowed(['jpg', 'png'], 'jpg or png only')


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
        required, min_4, max_50
        ])

    password = PasswordField("Password", validators=[
        required, min_4, max_80
        ])

    remember = BooleanField('Remember me')


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[
        required, min_4, max_50
        ])
    
    email = StringField("Email", validators=[
        required, 
        email_validator
        ])

    profile_image = FileField('Profile Photo', validators=[
                                optional, file
                                ])

    backdrop_image = FileField('Profile Background', validators=[
                                optional, file
                                ])

    password = PasswordField("Password", validators=[
        required, min_4, max_80
        ])
