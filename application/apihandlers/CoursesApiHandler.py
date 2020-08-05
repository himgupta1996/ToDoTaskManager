from application.db_schema import User, Course, Enrollment, ToDoTask, UserTaskAssociation
from application.apihandlers.AbstractApiHandler import *
from flask import render_template

class CoursesApiHandler(AbstractApiHandler):
	def __init(self, *args, **kargs):
		super(CoursesApiHandler, self).__init__(*args, **kargs)

	def get(self, term = None):

		if term == None:
			courseData = Course.objects.order_by("-courseID")
		else:
			courseData = Course.objects(term=term)
		return render_template("courses.html", courses = True, courseData = courseData, term = term)
