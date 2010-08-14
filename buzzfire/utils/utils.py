# A simple bunch of helpers

import redis
from buzzfire import settings


def check_auth(request):
	try:
		user_id = request.session['user_id']
		return True
	except KeyError:
		return False
		
def get_redis_conn():
	conn = redis.Redis(settings.BUZZ_REDIS_HOST, settings.BUZZ_REDIS_PORT)
	return conn
	