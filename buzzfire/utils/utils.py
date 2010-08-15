# A simple bunch of helpers

import redis
from buzzfire import settings


def check_auth(request):
	try:
		user_id = request.session['buzz_user_id']
		return True
	except KeyError:
		return False
		
def get_redis_conn():
	conn = redis.Redis(settings.BUZZ_REDIS_HOST, settings.BUZZ_REDIS_PORT)
	return conn
	

def convert_to_builtin_type(obj):
        
        if(not isinstance(obj, (list, set))):
                obj = [obj]
        result=[]
        for o in obj:
                d = { 'type':o.__class__.__name__
                      }
                d.update(o.__dict__)
                result.append(d)
        
        return result

