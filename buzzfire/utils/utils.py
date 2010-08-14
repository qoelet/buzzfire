# A simple bunch of helpers

def check_auth(request):
	try:
		user_id = request.session['user_id']
		return True
	except KeyError:
		return False