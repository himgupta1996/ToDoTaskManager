from application import app
from flask import render_template, request, Response, json, redirect, flash, url_for, session, Markup, jsonify
from .db_schema import User, Course, Enrollment, ToDoTask, UserTaskAssociation
from application.forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user
from application import login_manager
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from .constants import Constants
import application.constants as global_constants
import time
import configparser
from application.apihandlers.CoursesApiHandler import CoursesApiHandler
from application.apihandlers.ToDoDailyApiHandler import ToDoDailyApiHandler
from application.apihandlers.ToDoProgressApiHandler import ToDoProgressApiHandler
from application.apihandlers.ToDoAllApiHandler import ToDoAllApiHandler

courseData = [{"courseID":"1111","title":"PHP 111","description":"Intro to PHP","credits":"3","term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":"4","term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":"3","term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":"3","term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":"4","term":"Fall"}]

@login_manager.user_loader
def load_user(user_id):
	print("The user Id is %s" % (str(ObjectId(user_id))))
	return User.objects(id=ObjectId(user_id)).first()

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
	return render_template("index.html", index = True)

@app.route('/courses')
@app.route('/courses/<term>')
def courses(term = None):
	if not session.get('username'):
		flash(Markup('Kindly login to access To Do tasks section. If not registered yet, kindly register<a href = %s> here</a>.' % (url_for('register'))), "danger")
		return redirect(url_for('login'))

	user_id = session.get('user_id')
	if request.method.lower() == "get":
		obj = CoursesApiHandler(user_id = user_id)
		return obj.get(term= term)
	# if term == None:
	# 	courseData = Course.objects.order_by("-courseID")
	# else:
	# 	courseData = Course.objects(term=term)
	# return render_template("courses.html", courses = True, courseData = courseData, term = term)

@app.route('/register', methods = ["GET", "POST"])
def register():
	if session.get('username'):
		redirect(url_for('index'))
	form = RegisterForm()
	if form.validate_on_submit():
		print("I am in Validate.")
		user_id = User.objects.count()+1
		email = form.email.data
		password = form.password.data
		first_name = form.first_name.data
		last_name = form.last_name.data
		score = 0
		reward_points = 0

		user = User(user_id = user_id, email=email, first_name=first_name, last_name=last_name, score = score, reward_points = reward_points)
		user.set_password(password)
		user.save()
		flash("%s, You are successfully registered!." % (first_name), "success")
		return redirect(url_for('index'))
	return render_template("register.html", form= form, title="Register", register = True)

@app.route('/addnewtask')
def add_new_task():
	if not session.get('username'):
		flash(Markup('Kindly login to enroll for courses. If not registered yet, kindly register<a href = %s> here</a>.' % (url_for('register'))), "danger")
		return redirect(url_for('login'))
	form = AddNewTaskForm()

@app.route('/login', methods = ["GET", "POST"])
def login():
	if session.get('username'):
		return redirect(url_for('index'))
	form = LoginForm()
	email = form.email.data
	password = form.password.data
	user = User.objects(email=email).first()
	if form.validate_on_submit():
		if user and user.get_password(password):
			if form.remember_me.data:
				print("Yes remember me")
			login_user(user, remember = form.remember_me.data)
			flash("%s, You are successfully logged in!." % (user.first_name), "success")

			# Updating Constants by Loading config values
			config = configparser.ConfigParser()
			config.read('user_config.cfg')
			# global DAILY_TASK_DAYS_LIMITATION 
			# DAILY_TASK_DAYS_LIMITATION = int(config["user_info"]["daily_task_days_limitation"])
			global_constants.DAILY_TASK_DAYS_LIMITATION = int(config["user_info"]["daily_task_days_limitation"])
			print("The daily task limitations is %s" % (global_constants.DAILY_TASK_DAYS_LIMITATION))

			session["user_id"] = user.user_id
			session["username"] = user.first_name
			return redirect("/index")
		else:
			flash(Markup('Check your username or password. If not registered yet, kindly register<a href = %s> here</a>.' % (url_for('register'))), "danger")
			return render_template("login.html", form = form, title = "Login", login = True)

	return render_template("login.html", form = form, title = "Login", login = True)


@app.route('/logout')
def logout():
	logout_user()
	session['user_id'] = False
	session.pop('username', None)
	return redirect(url_for('index'))

@app.route('/enrollment', methods = ["GET", "POST"])
def enrollment():

	print("The session is %s" % (session.get('username')))

	if not session.get('username'):
		flash(Markup('Kindly login to enroll for courses. If not registered yet, kindly register<a href = %s> here</a>.' % (url_for('register'))), "danger")
		return redirect(url_for('login'))


	courseID = request.form.get('courseId')
	courseTitle = request.form.get('title')
	term = request.form.get("term")
	user_id = session.get('user_id')
	if courseID:
		if Enrollment.objects(user_id = user_id, courseID = courseID):
			flash("You have already registered for the course: %s" % (courseTitle), "success")
			return redirect(url_for("courses"))
		else:
			Enrollment(user_id = user_id, courseID = courseID).save()
			flash("Congratulations!! You have successfully enrolled for the course: %s" % (courseTitle), "success")
			return redirect(url_for("courses"))

	classes = list(User.objects.aggregate(*[
		    {
		        '$lookup': {
		            'from': 'enrollment', 
		            'localField': 'user_id', 
		            'foreignField': 'user_id', 
		            'as': 'r1'
		        }
		    }, {
		        '$unwind': {
		            'path': '$r1', 
		            'includeArrayIndex': 'r1_id', 
		            'preserveNullAndEmptyArrays': False
		        }
		    }, {
		        '$lookup': {
		            'from': 'course', 
		            'localField': 'r1.courseID', 
		            'foreignField': 'courseID', 
		            'as': 'r2'
		        }
		    }, {
		        '$unwind': {
		            'path': '$r2', 
		            'preserveNullAndEmptyArrays': False
		        }
		    }, {
		        '$match': {
		            'user_id': user_id
		        }
		    }, {
		        '$sort': {
		            'courseID': 1
		        }
		    }
		]))

	#data = {"id": request.args.get('courseId'), 'term': request.args.get('term'), 'title': request.args.get('title')}
	return render_template("enrollment.html", title = "Enrollment", classes = classes, enrollment=True)

@app.route('/responseapi/')
@app.route('/responseapi/<idx>')
def responseapi(idx=None):
	if idx==None:
		response = courseData
	else:
		response = courseData[int(idx)]
	return Response(json.dumps(response), mimetype= "application/json")

@app.route('/user')
@app.route('/user/<user_id>', methods = ["GET"])
def user(user_id = None):
	#User(id =21, first_name = "Himanshu", last_name = "Gupta", email = "himanshu.gupta@citrix.com", password = "abcd1234").save()
	if user_id:
		user = User.objects(user_id = user_id)[0]
		return jsonify(user), 200
	else:
		users = User.objects.all()
		print(users.__dict__)
		return render_template("user.html", users = users)

@app.route('/todo_main')
def todo_main():
	if not session.get('username'):
		flash(Markup('Kindly login to access To Do tasks section. If not registered yet, kindly register<a href = %s> here</a>.' % (url_for('register'))), "danger")
		return redirect(url_for('login'))

	user_id = session.get('user_id')

	# print(Constants.__dict__)
	# tasks = ToDoTask.objects(task_type = Constants.DAILY_TASK_TYPE, status = Constants.IN_PROGRESS_STATUS)
	# for task in tasks:
	# 	task_id = task.task_id
	# 	print("The task is %s" % (task))
	# 	date_added = datetime.strptime(task.date_added, '%Y-%m-%d')
	# 	date_current = datetime.today() 
	# 	deadline_date = datetime.strptime(task.deadline_date, '%Y-%m-%d')
	# 	##finding if it has been 7 days since the date added
	# 	if deadline_date > date_current:
	# 		task.update(status = Constants.FAILED_STATUS)

	# 	if (date_current-date_added).days > global_constants.DAILY_TASK_DAYS_LIMITATION:
	# 		print("greater than 7")
	# 		task.update(status = Constants.FAILED_STATUS)
	# 		user_task_association = UserTaskAssociation.objects(task_id = task_id, user_id = user_id)
	# 		user_task_association.update(user_task_score = 0)

	return render_template("selfDevelopmentTools/todo_landing.html", todo = True, user_id = user_id)

@app.route('/todo')
def todo():
	if not session.get('username'):
		flash(Markup('Kindly login to access To Do tasks section. If not registered yet, kindly register<a href = %s> here</a>.' % (url_for('register'))), "danger")
		return redirect(url_for('login'))
	placeholder_date = datetime.today().strftime('%Y-%m-%d')
	placeholder_month = datetime.today().strftime('%Y-%m')
	placeholder_year = datetime.today().strftime('%Y')

	##updating the database with appropriate task status
	# print(Constants.__dict__)
	# tasks = ToDoTask.objects(task_type = Constants.DAILY_TASK_TYPE, status = Constants.IN_PROGRESS_STATUS)
	# for task in tasks:
	# 	print("The task is %s" % (task))
	# 	date_added = datetime.strptime(task.date_added, '%Y-%m-%d')
	# 	date_current = datetime.today()
	# 	##finding if it has been 7 days since the date added
	# 	if (date_current-date_added).days > 7:
	# 		print("greater than 7")
	# 		task.update(status = Constants.FAILED_STATUS)

	return render_template("selfDevelopmentTools/todo_index.html", todo = True, todo_manage = True, placeholder = (str(placeholder_date), str(placeholder_month), \
		str(placeholder_year)), title = "Manage Your To Do Tasks")

# can remove get and post from first one
@app.route('/dailytodo', methods = ["GET", "POST", "PUT"])
@app.route('/dailytodo/<task_id>', methods = ["GET", "PUT", "DELETE"])
def dailytodo(task_id = None):
	if not session.get('username'):
		flash(Markup('Kindly login to access To Do tasks section. If not registered yet, kindly register<a href = %s> here</a>.' % (url_for('register'))), "danger")
		return redirect(url_for('login'))
	user_id = session.get('user_id')

	# for arg in request.args:
	# 	if arg not in Constants.TO_DO_DAILY_ARGS:
	# 		return jsonify("This api with the arg: %s is not supported" % (arg))

	tododailyobj = ToDoDailyApiHandler(user_id = user_id)

	if request.method.lower() == "delete":
		return tododailyobj.delete(task_id = task_id)

	if request.method.lower() == "put":
		return tododailyobj.put(task_id = task_id)

	if request.method.lower() == "post":
		print("Posting the request")
		return tododailyobj.post(task_id = task_id)

	if request.method.lower() == "get":
		return tododailyobj.get(task_id = task_id)

@app.route('/todo_progress')
def todo_progress():
	
	if not session.get('username'):
		flash(Markup('Kindly login to access To Do tasks section. If not registered yet, kindly register<a href = %s> here</a>.' % (url_for('register'))), "danger")
		return redirect(url_for('login'))
	user_id = session.get('user_id')

	todo_progress = ToDoProgressApiHandler(user_id = user_id)

	if request.method.lower() == "get":
		return todo_progress.get()

@app.route('/todo_all')
def todo_all():
	if not session.get('username'):
		flash(Markup('Kindly login to access To Do tasks section. If not registered yet, kindly register<a href = %s> here</a>.' % (url_for('register'))), "danger")
		return redirect(url_for('login'))

	user_id = session.get('user_id')
	todo_all = ToDoAllApiHandler(user_id = user_id)

	if request.method.lower() == "get":
		return todo_all.get()


@app.route('/completed_tasks')
def completed_tasks():
	pass
