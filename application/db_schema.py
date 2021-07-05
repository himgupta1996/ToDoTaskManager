from application import db
import flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Document):
	user_id = db.IntField(unique = True)
	first_name = db.StringField(max_length = 50)
	last_name = db.StringField(max_length = 50)
	email = db.StringField(max_length = 50, unique = True)
	password = db.StringField(max_length = 100)
	score = db.IntField()
	reward_points = db.IntField()

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def get_password(self, password):
		return check_password_hash(self.password, password)

class Course(db.Document):
	courseID = db.StringField(max_length = 10, unique = True)
	title = db.StringField(max_length = 100)
	description = db.StringField(max_length = 255)
	credits = db.IntField()
	term = db.StringField(max_length = 25)

class Enrollment(db.Document):
	user_id = db.IntField()
	courseID = db.StringField(max_length = 10)

class ToDoTask(db.Document):
	task_id = db.IntField(unique = True)
	title = db.StringField(max_length = 255, required = True)
	date_added = db.StringField(max_length = 10)
	date_started = db.StringField(max_length = 10)
	deadline_date = db.StringField(max_length = 10)
	completion_date = db.StringField(max_length = 10)
	description = db.StringField(max_length = 255)
	task_type = db.StringField(max_length = 10, required= True)
	status = db.StringField(max_length = 15)
	time_taken = db.StringField(max_length = 15)
	days_taken = db.IntField()
	priority = db.StringField(max_length = 5)

class UserTaskAssociation(db.Document):
	user_id = db.IntField()
	task_id = db.IntField()
	task_score = db.IntField()
	task_reward_points = db.IntField()


