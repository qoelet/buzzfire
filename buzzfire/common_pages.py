from django.shortcuts import render_to_response
from django.template import RequestContext

from buzzfire.utils.utils import check_auth

def homepage(request):
	auth_status = check_auth(request)
	
	if auth_status:
		buzz_auth = True
	else:
		buzz_auth = None
		
	return render_to_response('common_pages/homepage.html', {'buzz_auth':buzz_auth}, context_instance=RequestContext(request))
	
def faq(request):
	auth_status = check_auth(request)
	
	if auth_status:
		buzz_auth = True
	else:
		buzz_auth = None
		
	return render_to_response('common_pages/faq.html', {'buzz_auth':buzz_auth}, context_instance=RequestContext(request))