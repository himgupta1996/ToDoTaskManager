from application.db_schema import User, Course, Enrollment, ToDoTask, UserTaskAssociation
from application.apihandlers.AbstractApiHandler import *
import application.constants as global_constants
# from flask import render_template

class ToDoAllApiHandler(AbstractApiHandler):
	def __init__(self, *args, **kargs):
		super(ToDoAllApiHandler, self).__init__(*args, **kargs)

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

	def check_task_expiry_and_get_status(self, task):
		date_added = datetime.strptime(task["e2"]["date_added"], '%Y-%m-%d')
		deadline_date = datetime.strptime(task["e2"]["deadline_date"], '%Y-%m-%d')
		priority = task["e2"]["priority"].upper()
		current_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d')
		days_difference = (current_date-date_added).days
		expected_days_difference = (deadline_date-date_added).days
		days_left = (deadline_date-current_date).days
		print("The deadline are %s" % deadline_date)
		print("The today are %s" % current_date)
		print("The days left are %s" % days_left)
		print("The days_difference is %s" % (days_difference))
		# PRIORITY_VALUE_MAPPING = {PRIORITY_P1: 5, PRIORITY_P2: 3, PRIORITY_P3: 2, PRIORITY_P4: 1}
		print("The task is %s" % (task["e2"]["title"]))
		print(((Constants.PRIORITY_VALUE_MAPPING[Constants.PRIORITY_P1]-Constants.PRIORITY_VALUE_MAPPING[priority])+expected_days_difference))
		if days_difference > ((Constants.PRIORITY_VALUE_MAPPING[Constants.PRIORITY_P1]-Constants.PRIORITY_VALUE_MAPPING[priority])+expected_days_difference):
			user = User.objects(user_id = self.user_id).first()
			score = int(user.score)
			score_update = score-Constants.PRIORITY_VALUE_MAPPING[priority] if score-Constants.PRIORITY_VALUE_MAPPING[priority] > 0 else 0 
			user.update(score = score_update)

			user_task_association = UserTaskAssociation.objects(task_id = task["e2"]["task_id"], user_id = self.user_id)
			user_task_association.update(task_score = -1*Constants.PRIORITY_VALUE_MAPPING[priority], task_reward_points = 0)

			todotask = ToDoTask.objects(task_id = task["e2"]["task_id"])[0]
			todotask.update(status = Constants.FAILED_STATUS)

			return Constants.FAILED_STATUS, None
		else:
			return task["e2"]["status"], days_left

	def get(self):

		match_dict = {'user_id': self.user_id}
		total_tasks = self._get_user_task_information(match_dict)

		print("The request args are %s" % (list(request.args)))
		print("grace %s" % (request.args.get("Grace")))

		filter_dict = {}
		
		task_title = request.args.get("task_title")
		filter_dict["task_title"] = task_title
		task_statuses = request.args.getlist("task_status")
		filter_dict["task_statuses"] = task_statuses
		task_priorities = request.args.getlist("priority")
		filter_dict["task_priorities"] = task_priorities
		start_date = request.args.get("start_date")
		filter_dict["start_date"] = start_date
		deadline_date = request.args.get("deadline_date")
		filter_dict["deadline_date"] = deadline_date
		grace = request.args.get("Grace")
		filter_dict["Grace"] = grace

		filter_tasks = []
		for task in total_tasks:
			if task_title and task_title not in task["e2"]["title"]:
				continue
			##checking if the task has crossed the expiry date
			task["e2"]["status"], task["e2"]["days_left"] = self.check_task_expiry_and_get_status(task)

			if task_statuses and task["e2"]["status"] not in task_statuses:
				continue
			if task_priorities and task["e2"]["priority"] not in task_priorities:
				continue
			if start_date and start_date != task["e2"]["date_added"]:
				continue
			if grace and (task["e2"]["status"] != Constants.IN_PROGRESS_STATUS or task["e2"]["days_left"] > 0):
				continue
			if deadline_date and task["e2"]["deadline_date"] != deadline_date:
				continue
			print(task)
			filter_tasks.append(task)

		for task in filter_tasks:
			if task["e2"]["status"] == Constants.IN_PROGRESS_STATUS:			
				date_added = datetime.strptime(task["e2"]["date_added"], '%Y-%m-%d')
				date_current = datetime.today()
				days_difference = (date_current-date_added).days
				task["e2"]["days_taken"] = days_difference+1

		return render_template("selfDevelopmentTools/todo_add_view_all.html", todo = True, todo_all = True, total_tasks = filter_tasks, filter_dict= filter_dict, user_id = self.user_id)