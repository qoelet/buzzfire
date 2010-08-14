from django.shortcuts import render_to_response
from django.template import RequestContext

def homepage(request):
	return render_to_response('common_pages/homepage.html', {}, context_instance=RequestContext(request))
	
def faq(request):
	return render_to_response('common_pages/faq.html', {}, context_instance=RequestContext(request))