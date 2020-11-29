
from application.db_schema import User, Course, Enrollment, ToDoTask, UserTaskAssociation
from application.apihandlers.AbstractApiHandler import *
# from flask import render_template

class ToDoDailyApiHandler(AbstractApiHandler):
	def __init__(self, *args, **kargs):
		super(ToDoDailyApiHandler, self).__init__(*args, **kargs)

	def _get_user_task_information(self, match_dict):
		tasks = list(User.objects.aggregate(*[
		    {
		        '$lookup': {
		            'from': 'user_task_association', 
		            'localField': 'user_id', 
		            'foreignField': 'user_id', 
		            'as': 'e1'
		        }
		    }, {
		        '$unwind': {
		            'path': '$e1', 
		            'includeArrayIndex': 'e1_id', 
		            'preserveNullAndEmptyArrays': False
		        }
		    }, {
		        '$lookup': {
		            'from': 'to_do_task', 
		            'localField': 'e1.task_id', 
		            'foreignField': 'task_id', 
		            'as': 'e2'
		        }
		    }, {
		        '$unwind': {
		            'path': '$e2', 
		            'preserveNullAndEmptyArrays': False
		        }
		    }, {
		        '$match': match_dict
		    }
		]))
		return tasks


	def get(self, task_id = None):
		if task_id:
			print("The task in get is %s" % (task_id))
			task = ToDoTask.objects(task_id=str(task_id)).first()
			response = {"status": task.status, "description": task.description, "date_added":task.date_added, "title": task.title, "date_started": task.date_started}
			print("the task is %s" %(response))
			return jsonify(response), 200
		else:
			print("The request args are %s" % request.args)

			
			# date = request.args["date"]

			# date_request = datetime.strptime(date, '%Y-%m-%d')
			# date_current = datetime.today()
			# days_difference = (date_current-date_request).days

			# print("days_difference is %s" % (days_difference))

			# if days_difference == 0:
			# 	match_dict = {'user_id': self.user_id, 'e2.status': Constants.IN_PROGRESS_STATUS}
			# 	tasks = self._get_user_task_information(match_dict)
			# 	return render_template("selfDevelopmentTools/todo_daily.html", todo =  True, tasks = tasks, date = date)

			# elif days_difference > 0:
			# 	print("I am here.")
			# 	flash(Markup('You don\'t have access to tasks which are finished on back date. If you want to access those tasks, kindly check your finished/failed tasks section <a href = %s> here</a>.' % (url_for('completed_tasks'))), "danger")
			# 	return redirect(url_for("todo"))

			# elif days_difference < 0:
			# 	match_dict = {'user_id': self.user_id, 'e2.status': Constants.YET_TO_START_STATUS, 'e2.date_added': date}
			# 	tasks = self._get_user_task_information(match_dict)
			return render_template("selfDevelopmentTools/todo_daily.html", todo = True, tasks = tasks, date = date)

	def delete(self, task_id = None):
		try:
			if task_id:
				task = ToDoTask.objects(task_id=task_id).first()
				task.delete()
				association = UserTaskAssociation.objects(user_id=self.user_id, task_id=task_id).first()
				association.delete()
				return "DELETE call successful."
			else:
				return "DELETE call unsuccessful. Please include task_id.", 500
		except Exception as e:
			return jsonify("DELETE call unsuccessful. Error: %s" % (str(e))), 500

	def put(self, task_id = None):
		try:
			print("The request data is %s" % (request.form))
			if "status" not in request.form:
				return "PUT call unsuccessful. Only status is allowed as attribute in the URL argument."
			task_status = request.form["status"]
			if task_id:
				print("the task_id is %s" % (task_id))
				print("the type of task_id is %s" % (type(task_id)))
				task = ToDoTask.objects(task_id=task_id).first()
				if task_status == Constants.COMPLETED_STATUS:
					date_added = datetime.strptime(task.date_added, '%Y-%m-%d')
					date_current = datetime.today()
					days_difference = (date_current-date_added).days
					user_task_association = UserTaskAssociation.objects(task_id = task_id, user_id = self.user_id)
					user_task_association.update(user_task_score = ((Constants.DAILY_TASK_DAYS_TAKEN_UPPER_BOUND - (days_difference + 1))*100)//Constants.DAILY_TASK_DAYS_TAKEN_UPPER_BOUND)
					# if the user completes the task on the same day, it is counted as 1 day, if on 2nd day, it is counted as 2 days
					# therefore we are adding the 1 to the days_difference
					task.update(days_taken = days_difference+1)
				task.update(status = task_status)
				return "PUT call successful."
			else:
				return "PUT call unsuccessful. Please include task_id in URL."
		except Exception as e:
			raise e

	def post(self, task_id = None):
		try:
			# print("The request data is %s" % (request.form))
			# task_data = request.form
			# task_id = int(round(time.time() * 1000))
			# date = task_data["date"]
			# date_request = datetime.strptime(date, '%Y-%m-%d')
			# date_current = datetime.today()
			# days_difference = (date_current-date_request).days
			# if days_difference == 0:
			# 	ToDoTask(task_id = task_id, title = task_data["title"], date_added = task_data["date"], date_started = task_data["date"], description=task_data["description"], task_type = "Daily", status = Constants.IN_PROGRESS_STATUS).save()
			# 	UserTaskAssociation(user_id = self.user_id, task_id = task_id).save()
			# 	return jsonify(task_id)
			# elif days_difference < 0:
			# 	ToDoTask(task_id = task_id, title = task_data["title"], date_added = task_data["date"], description=task_data["description"], task_type = "Daily", status = Constants.YET_TO_START_STATUS).save()
			# 	UserTaskAssociation(user_id = self.user_id, task_id = task_id).save()
			# 	return jsonify(task_id)
			# elif days_difference > 0:
			# 	flash(Markup('You don\'t have access to post tasks which on back date. You can access you past finished/failed tasks section <a href = %s> here</a>.' % (url_for('completed_tasks'))), "danger")
			# 	return redirect(url_for("todo"))
			print("The request data is %s" % (request.form))
			task_data = request.form
			task_id = int(round(time.time() * 1000))
			deadlinedate = task_data["deadline"]
			# deadlinedate = datetime.strptime(deadlinedate, '%Y-%m-%d')
			date_current = datetime.today().strftime('%Y-%m-%d')
			# days_to_complete = (deadlinedate-date_current).days
			print("I am here")
			print("date %s %s" % (date_current, deadlinedate))
			ToDoTask(task_id = task_id, title = task_data["title"], date_added = str(date_current), date_started = str(date_current), description=task_data["description"], task_type = "Daily", status = Constants.IN_PROGRESS_STATUS, priority= task_data["priority"], deadline_date = str(deadlinedate)).save()
			UserTaskAssociation(user_id = self.user_id, task_id = task_id).save()
			print("I am here 2")
			return jsonify(task_id)

		except Exception as e:
			return jsonify("The POST call failed. Error: %s" % (str(e))), 500

