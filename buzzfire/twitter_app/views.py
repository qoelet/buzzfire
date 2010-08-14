from django.http import HttpResponseRedirect

import urlparse
import oauth2 as oauth

from buzzfire.twitter_app.models import User
from buzzfire.twitter_app.dao import UserDao
from buzzfire.utils.utils import check_auth, get_redis_conn
from buzzfire import settings, buzz_secrets

OAUTH_CALLBACK_URL = "http://buzz-fire.com/twitter/oauth_callback"
REQUEST_TOKEN_URL = "http://twitter.com/oauth/request_token"
ACCESS_TOKEN_URL = "http://twitter.com/oauth/access_token"
AUTHORIZE_URL = "http://twitter.com/oauth/authorize"

# AUTH VIEWS

def login(request):
	consumer = oauth.Consumer(buzz_secrets.CONSUMER_KEY, buzz_secrets.CONSUMER_SECRET)
	client = oauth.Client(consumer)
	
	# Get request token
	resp, content = client.request(REQUEST_TOKEN_URL, "GET")
	try:
		if resp['status'] != '200':
			error_message = "Invalid response received: %s" % resp['status']
	except KeyError:
		raise Exception('Did not get a proper response')
		
	# store to session store
	request.session['request_token'] = dict(urlparse.parse_qsl(content))
	
	auth_url = "%s?oauth_token=%s" % (AUTHORIZE_URL, request.session['request_token']['oauth_token'])
	
	return HttpResponseRedirect(url)
	
def logout(request):
	pass
	
def auth_user(request):
	token = oauth.Token(request.session['request_token']['oauth_token'], request.session['request_token']['oauth_token_secret'])
	
	resp, content = client.request(ACCESS_TOKEN_URL, "GET")
	if resp['status'] != 200:
		raise Exception("Invalid response from Twitter.")
		
	access_token = dict(urlparse.parse_qsl(content))
	
	# Lookup user or create
	conn = get_redis_conn()
	user_dao = UserDao(conn)
	user_id = access_token['user_id']
	user_exists = user_dao.get_user_id(user_id)
	if user_exists == None:
		# create user
		screen_name = access_token['screen_name']
		new_user = User(screen_name, user_id, oauth_token_secret=access_token['oauth_token_secret'], oauth_token=access_token['oauth_token'])
		user_dao.save(new_user)
	else:
		# update existing user
		user = user_dao.get_user(user_id)
		user.oauth_token_secret = access_token['oauth_token_secret']
		user.oauth_token = oauth_token=access_token['oauth_token']
		user_dao.save(user)
	
	# redirect to user homepage
	return HttpResponse(settings.BUZZFIRE_USER_PAGE)
	
def mybuzz(request):
	# Get user's timeline
	return render_to_response('mybuzz/homepage.html', {}, context_instance=RequestContext(request))
	
# DATA GET VIEWS

def get_timeline(request):
	auth_status = check_auth(request)
	
	if auth_status:
		return True
	else:
		return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)