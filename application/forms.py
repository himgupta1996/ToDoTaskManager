from flask_wtf import FlaskForm 
from wtforms import StringField, BooleanField, SubmitField, PasswordField, RadioField, DateField
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

class AddNewTaskForm(FlaskForm):
	task_title = StringField("Task Title", validators = [DataRequired()])
	task_description = StringField("Task Description", validators = [DataRequired()])
	priority =  RadioField('Priority', choices=[('P1','Top Priority'),('P2','Second Most Priority'), ('P3', 'Third Most Pririty'), ('P4, Last Priority')])
	deadline_date = DateField('Deadline Date ', format="'%d/%m/%Y'", validators = [DataRequired()])
	submit = SubmitField("Add")

class FilterTaskForm(FlaskForm):
	task_title = StringField("Task Title")
	task_description = StringField("Task Description")
	priority =  RadioField('Priority', choices=[('P1','Top Priority'),('P2','Second Most Priority'), ('P3', 'Third Most Pririty'), ('P4, Last Priority')])
	start_date = DateField('Start Date ', format="'%d/%m/%Y'")
	submit = SubmitField("Filter")



