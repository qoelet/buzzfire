from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext

import urlparse
import oauth2 as oauth
import urllib

from buzzfire.twitter_app.models import User
from buzzfire.twitter_app.dao import UserDao
from buzzfire.utils.utils import check_auth, get_redis_conn
from buzzfire import settings, buzz_secrets

OAUTH_CALLBACK_URL = "http://buzz-fire.com/twitter/oauth_callback"
REQUEST_TOKEN_URL = "http://twitter.com/oauth/request_token"
ACCESS_TOKEN_URL = "http://twitter.com/oauth/access_token"
AUTHORIZE_URL = "http://twitter.com/oauth/authorize"
USER_TIMELINE_URL ="http://api.twitter.com/1/statuses/home_timeline.json"
SEARCH_URL="http://search.twitter.com/search.json?result_type=mixed"
STATUS_UPDATE_URL="http://api.twitter.com/1/statuses/update.json"

# AUTH VIEWS
consumer = oauth.Consumer(buzz_secrets.CONSUMER_KEY, buzz_secrets.CONSUMER_SECRET)
client = oauth.Client(consumer)


def login(request): 
	   
	# Get request token
	resp, content = client.request(REQUEST_TOKEN_URL, "GET")
	try:
		if resp['status'] != '200':
			error_message = "Invalid response received: %s" % resp['status']
	except KeyError:
		error_message = "No data received."
		
	# store to session store
	request.session['request_token'] = dict(urlparse.parse_qsl(content))
	
	auth_url = "%s?oauth_token=%s" % (AUTHORIZE_URL, request.session['request_token']['oauth_token'])
	
	return HttpResponseRedirect(auth_url)

def logout(request):
	try:
		del request.session['buzz_user_id']
	except KeyError:
		pass
		
	return HttpResponseRedirect(settings.BUZZFIRE_HOME_PAGE)

def auth_user(request):
	token = oauth.Token(request.session['request_token']['oauth_token'], request.session['request_token']['oauth_token_secret'])

	auth_client = oauth.Client(consumer, token)
	
	resp, content = auth_client.request(ACCESS_TOKEN_URL, "GET")


	if resp['status'] != '200':
		
		raise Exception("Invalid response from Twitter.")
		
	access_token = dict(urlparse.parse_qsl(content))
	
	# Lookup user or create
	conn = get_redis_conn()
	user_dao = UserDao(conn)

	user_id = user_dao.get_user_id(access_token['screen_name'])
	if user_id == None:
		# create user

		screen_name = access_token['screen_name']
		new_user = User(screen_name, user_id, oauth_token_secret=access_token['oauth_token_secret'], oauth_token=access_token['oauth_token'])
		user_id=user_dao.save(new_user)
	else:
		# update existing user
		user = user_dao.get_user(user_id)
		user.oauth_token_secret = access_token['oauth_token_secret']
		user.oauth_token = oauth_token=access_token['oauth_token']
		user_id=user_dao.save(user)
		
	request.session['buzz_user_id'] = user_id
	
	# redirect to user homepage
	return HttpResponseRedirect(settings.BUZZFIRE_USER_PAGE)

def mybuzz(request):
	auth_status = check_auth(request)
	
	if auth_status:
		buzz_auth = True
	else:
		buzz_auth = None
	
	return render_to_response('mybuzz/homepage.html', {'buzz_auth':buzz_auth}, context_instance=RequestContext(request))

# DATA GET VIEWS

def get_timeline(request):
	auth_status = check_auth(request)
	
	if auth_status:
		user_id = request.session['buzz_user_id']

		conn = get_redis_conn()
		user_dao = UserDao(conn)

		user = user_dao.get_user(user_id)
		oauth_token = user.oauth_token

		oauth_token_secret = user.oauth_token_secret
		authorized_token = oauth.Token(oauth_token, oauth_token_secret)
		user_client =oauth.Client(consumer, authorized_token)
		resp, content = user_client.request(USER_TIMELINE_URL)
		try:
				if resp['status'] != '200':
						error_message = "Invalid response received: %s" % resp['status']
		except KeyError:
				raise Exception('Did not get a proper response')
		return HttpResponse(content)
	else:
		return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)


def search(request, query_string):
	auth_status = check_auth(request)
	if auth_status:
		user_id = request.session['buzz_user_id']
		
		conn = get_redis_conn()
		user_dao = UserDao(conn)
		
		user = user_dao.get_user(user_id)
		oauth_token = user.oauth_token

		oauth_token_secret = user.oauth_token_secret
		authorized_token = oauth.Token(oauth_token, oauth_token_secret)
		user_client =oauth.Client(consumer, authorized_token)
		q = urllib.urlencode({"q":query_string})
		search_url = SEARCH_URL+"&"+q
		resp, content = user_client.request(search_url)
		try:
				if resp['status'] != '200':
						error_message = "Invalid response received: %s" % resp['status']
		except KeyError:
				raise Exception('Did not get a proper response')
		return HttpResponse(content)
	else:
		return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)

				

def update_status(request):
	auth_status = check_auth(request)
	if auth_status:
		user_id = request.session['buzz_user_id']

		if request.method == 'POST':
				status = request.POST['status']
		if request.POST.has_key('tweet_id'):
			tweet_id = request.POST['tweet_id']
		else:
			tweet_id =None
					
			conn = get_redis_conn()
			user_dao = UserDao(conn)
	
			user = user_dao.get_user(user_id)
			oauth_token = user.oauth_token
			
			oauth_token_secret = user.oauth_token_secret
			authorized_token = oauth.Token(oauth_token, oauth_token_secret)
			user_client =oauth.Client(consumer, authorized_token)
		if tweet_id:
			q = urllib.urlencode({"status":status, "in_reply_to_status_id":tweet_id})
		else:
			q =urllib.urlencode({"status":status})
		
		resp, content = user_client.request(STATUS_UPDATE_URL, method="POST", body=q)	 
		try:
			if resp['status'] != '200':
				error_message = "Invalid response received: %s" % resp['status']
			else:
				return HttpResponse()
		except KeyError:
				raise Exception('Did not get a proper response')
				return HttpResponse('{"status":"Success"}')
	else:
			return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)
