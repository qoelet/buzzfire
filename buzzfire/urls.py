from django.conf.urls.defaults import *
from buzzfire import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # temp serves for media
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT, 'show_indexes':True}),
	
	# authentication
	(r'^login/$', 'buzzfire.twitter_app.views.login'),
	(r'^logout/$', 'buzzfire.twitter_app.views.logout'),
	
	# user_page
	(r'^mybuzz/$', 'buzzfire.twitter_app.views.mybuzz'),
	
	# FAQ
	(r'^faq/$', 'buzzfire.common_pages.faq'),
	
	# homepage
	(r'^$', 'buzzfire.common_pages.homepage'),
)
