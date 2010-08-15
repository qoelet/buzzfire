from django.conf.urls.defaults import *
from buzzfire import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # temp serves for media
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT, 'show_indexes':True}),
    
    # authentication
    url(r'^login/$', 'buzzfire.twitter_app.views.login'),
    url(r'^logout/$', 'buzzfire.twitter_app.views.logout'),
    url(r'^authenticated/$', 'buzzfire.twitter_app.views.auth_user'),
    url(r'^timeline/$', 'buzzfire.twitter_app.views.get_timeline', name="mybuzz_timeline"),               
    url(r'^search/(\w+)$', 'buzzfire.twitter_app.views.search'),
    url(r'^update/$', 'buzzfire.twitter_app.views.update_status'),
    url(r'^comment/add/$', 'buzzfire.comment_app.views.add'),
    url(r'^comment/get/(\w+)$', 'buzzfire.comment_app.views.get'),
    url(r'^comment/get/bookmark/(\w+)$', 'buzzfire.comment_app.views.get_bookmark_comment'),
    url(r'^comment/delete/(\w+)$', 'buzzfire.comment_app.views.delete'),
                       
    url(r'^bookmark/add/$', 'buzzfire.bookmark_app.views.add', name="mybuzz_add_bookmark"),
    url(r'^bookmark/user/(\w+)$', 'buzzfire.bookmark_app.views.get_user_bookmark'),
    url(r'^bookmark/tag/(\w+)$', 'buzzfire.bookmark_app.views.tag_bookmark'),                      
    url(r'^bookmark/untag/(\w+)$', 'buzzfire.bookmark_app.views.untag_bookmark'),                      
    url(r'^bookmark/delete/(\w+)$', 'buzzfire.bookmark_app.views.delete_bookmark'),                      
    # user_page
    url(r'^mybuzz/$', 'buzzfire.twitter_app.views.mybuzz'),
    
    # FAQ
    url(r'^faq/$', 'buzzfire.common_pages.faq'),

    # homepage
    url(r'^$', 'buzzfire.common_pages.homepage'),
)
