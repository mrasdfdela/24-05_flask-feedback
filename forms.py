from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired

class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email")
    first_name = StringField("First Name")
    last_name = StringField("Last Name")

class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = TextField("Content", validators=[InputRequired()])
    username = StringField("User")