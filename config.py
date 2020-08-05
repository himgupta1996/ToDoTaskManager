import os
from datetime import timedelta

class Config(object):
	SECRET_KEY = os.environ.get("SECRET_KEY", b'_%\x14\x9c\x06\xf2!\xdb\x0eZ\xb9\x80\xb5\xc3\xfd\x94')
	#USE_SESSION_FOR_NEXT = True
	#REMEMBER_COOKIE_DURATION = timedelta(20)
	MONGODB_SETTINGS = {'db' : 'UTA_Enrollment',
						'host': 'mongodb://localhost:27017/UTA_Enrollment'}
