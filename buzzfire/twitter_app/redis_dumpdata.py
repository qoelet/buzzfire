# Dump some fake data to redis and test DAO (in place of dumpdata)

import simplejson as json
import redis

from models import User
from dao import UserDao

def dumpdata():
	json_file = open('fixtures/fakers.json', 'r')
	json_string = ''
	for line in json_file:
		json_string += line
	fake_data = json.loads(json_string)
	
	# dump to redis
	r = redis.Redis()
	user_ids = []
	for faker in fake_data:
		user = User(faker['screen_name'], faker['user_id'], oauth_token_secret=faker['oauth_token_secret'], oauth_token=faker['oauth_token'])
		user_dao = UserDao(r)
		user_id = user_dao.save(user)
		user_ids.append(user_id)
		
	# test DAO get
	test(user_ids)
		
	
		
def test(user_ids):
	# user_ids is an array of ids []
	r = redis.Redis()
	user_dao = UserDao(r)
	
	for user in user_ids:
		got_user = user_dao.get_user(user)
		print "Here's a user..."
		print got_user.screenname
		print got_user.id
		print got_user.oauth_token_secret
		print got_user.oauth_token
		print "-end-"
	
		
if __name__ == '__main__':
	dumpdata()
