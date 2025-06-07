from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6)])
    role = SelectField("Role", choices=[("student", "Student"), ("staff", "Staff")])
    submit = SubmitField("Register")
