from flask_wtf import FlaskForm 
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.db_schema import User

class LoginForm(FlaskForm):
	email = StringField("Email Id", validators = [DataRequired(), Email()])
	password = PasswordField("Password", validators = [DataRequired(), Length(min=6, max=15)])
	remember_me = BooleanField("Remember Me")
	submit = SubmitField("Login")

class RegisterForm(FlaskForm):
	email = StringField("Email Id", validators = [DataRequired(), Email()])
	password = PasswordField("Password", validators = [DataRequired(), Length(min=6, max=15)])
	password_confirm = PasswordField("Confirm Password", validators = [DataRequired(), Length(min=6, max=15), EqualTo('password')])
	first_name  = StringField("First Name", validators = [DataRequired(), Length(min=1, max=55)])
	last_name  = StringField("Last Name", validators = [DataRequired(), Length(min=1, max=55)])
	submit = SubmitField("Register Now")

	def validate_email(self, email):
		user = User.objects(email=email.data).first()
		if user:
			raise ValidationError("Email is already in Use. Pick another one")
