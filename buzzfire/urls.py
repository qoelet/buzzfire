from django.conf.urls.defaults import *
from buzzfire import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # temp serves for media
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
	
	# homepage
	(r'^$', 'buzzfire.common_pages.homepage'),
)
