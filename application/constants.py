class Constants(object):
	IN_PROGRESS_STATUS = "In Progress" 
	COMPLETED_STATUS = "Completed"
	FAILED_STATUS = "Failed"
	YET_TO_START_STATUS = "Yet To Start"
	DAILY_TASK_TYPE = "Daily"

	TO_DO_DAILY_ARGS = ["date"]

	global DAILY_TASK_DAYS_LIMITATION
	DAILY_TASK_DAYS_LIMITATION = 7
	DAILY_TASK_DAYS_TAKEN_UPPER_BOUND = 15

	PRIORITY_P1 = "P1"
	PRIORITY_P2 = "P2"
	PRIORITY_P3 = "P3"
	PRIORITY_P4 = "P4"
	PRIORITY_VALUE_MAPPING = {PRIORITY_P1: 5, PRIORITY_P2: 3, PRIORITY_P3: 2, PRIORITY_P4: 1}

