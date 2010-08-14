from django.http import HttpResponseRedirect

import oauth2 as oauth

from buzzfire.twitter_app.dao import UserDao
from buzzfire.utils.utils import check_auth
from buzzfire import settings, buzz_secrets

OAUTH_CALLBACK_URL = "http://buzz-fire.com/twitter/oauth_callback"
REQUEST_TOKEN_URL = "http://twitter.com/oauth/request_token"
ACCESS_TOKEN_URL = "http://twitter.com/oauth/access_token"
AUTHORIZE_URL = "http://twitter.com/oauth/authorize"

def login(request):
	consumer = oauth.Consumer(buzz_secrets.CONSUMER_KEY, buzz_secrets.CONSUMER_SECRET)
	client = oauth.Client(consumer)
	
def logout(request):
	pass

def get_timeline(request):
	auth_status = check_auth(request)
	
	if auth_status:
		return True
	else:
		return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)