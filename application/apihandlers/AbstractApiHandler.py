from flask import render_template, request, Response, json, redirect, flash, url_for, session, Markup, jsonify
from application.db_schema import User, Course, Enrollment, ToDoTask, UserTaskAssociation
from datetime import datetime, timedelta
from application.constants import Constants
import application.constants as global_constants
import time
class AbstractApiHandler():
	def __init__(self, *args, **kargs):
		self.user_id = kargs['user_id']
		# tasks = ToDoTask.objects(task_type = Constants.DAILY_TASK_TYPE, status = Constants.IN_PROGRESS_STATUS)
		# for task in tasks:
		# 	task_id = task.task_id
		# 	print("The task is %s" % (task))
		# 	date_added = datetime.strptime(task.date_added, '%Y-%m-%d')
		# 	date_current = datetime.today()
		# 	##finding if it has been 7 days since the date added
		# 	if (date_current-date_added).days > global_constants.DAILY_TASK_DAYS_LIMITATION:
		# 		print("greater than 7")
		# 		task.update(status = Constants.FAILED_STATUS)
		# 		user_task_association = UserTaskAssociation.objects(task_id = task_id, user_id = user_id)
		# 		user_task_association.update(user_task_score = 0)
		