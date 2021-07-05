from application.db_schema import User, Course, Enrollment, ToDoTask, UserTaskAssociation
from application.apihandlers.AbstractApiHandler import *
import application.constants as global_constants
# from flask import render_template

class ToDoProgressApiHandler(AbstractApiHandler):
	def __init__(self, *args, **kargs):
		super(ToDoProgressApiHandler, self).__init__(*args, **kargs)

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

	def get(self):

		match_dict = {'user_id': self.user_id}
		total_tasks = self._get_user_task_information(match_dict)
		total_tasks_count = len(total_tasks)

		match_dict = {'user_id': self.user_id, 'e2.status': Constants.IN_PROGRESS_STATUS}
		inprogress_tasks = self._get_user_task_information(match_dict)
		inprogress_tasks_count = len(inprogress_tasks)

		match_dict = {'user_id': self.user_id, 'e2.status': Constants.COMPLETED_STATUS}
		completed_tasks = self._get_user_task_information(match_dict)
		completed_tasks_count = len(completed_tasks)

		match_dict = {'user_id': self.user_id, 'e2.status': Constants.FAILED_STATUS}
		failed_tasks = self._get_user_task_information(match_dict)
		failed_tasks_count = len(failed_tasks)

		match_dict = {'user_id': self.user_id, 'e2.status': Constants.YET_TO_START_STATUS}
		yet_to_start_tasks = self._get_user_task_information(match_dict)
		yet_to_start_tasks_count = len(yet_to_start_tasks)

		completed_task_labels = [str(i) for i in range(1,global_constants.DAILY_TASK_DAYS_LIMITATION + 1)]
		completed_task_values = [0]*global_constants.DAILY_TASK_DAYS_LIMITATION

		for task in completed_tasks:
			print("The task is %s" % (task))

			completed_task_values[int(6) - 1] += 1
		print("The completed list %s" % (completed_task_values))

		inprogress_task_labels = [str(i) for i in range(1,global_constants.DAILY_TASK_DAYS_LIMITATION + 1)]
		inprogress_task_values = [0]*global_constants.DAILY_TASK_DAYS_LIMITATION
		for task in inprogress_tasks:			
			date_added = datetime.strptime(task["e2"]["date_added"], '%Y-%m-%d')
			date_current = datetime.today()
			days_difference = (date_current-date_added).days
			inprogress_task_values[days_difference] += 1

		# for i in range(1, DAILY_TASK_DAYS_LIMITATION+1):
		# 	match_dict = {'user_id': self.user_id, 'e2.status': Constants.COMPLETED_STATUS, 'e2.days_taken': i}
		# 	completed_tasks = self._get_user_task_information(match_dict)
		# 	completed_task_values.append(len(completed_tasks))
		# 	completed_tasks_count = len(completed_tasks)



		labels = [Constants.IN_PROGRESS_STATUS, Constants.COMPLETED_STATUS, Constants.FAILED_STATUS, Constants.YET_TO_START_STATUS]
		values = [inprogress_tasks_count, completed_tasks_count, failed_tasks_count, yet_to_start_tasks_count]
		
		total_task_pie_values = [float(inprogress_tasks_count)/total_tasks_count*100, 
			float(completed_tasks_count)/total_tasks_count*100,
			float(failed_tasks_count)/total_tasks_count*100,
			float(yet_to_start_tasks_count)/total_tasks_count*100]

		colors = ["#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA"]

		return render_template("selfDevelopmentTools/todo_progress.html", \
			todo = True, \
			todo_progress = True, \
			title='Your Tasks Stats', \
			max=10, \
			labels=labels, \
			values=values, \
			colors = colors, \
			user_id = self.user_id, \
			completed_task_labels = completed_task_labels, \
			completed_task_values = completed_task_values, \
			total_task_pie_values = total_task_pie_values, \
			inprogress_task_values = inprogress_task_values, \
			inprogress_task_labels = inprogress_task_labels)