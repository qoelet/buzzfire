from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.http import Http404

from buzzfire.bookmark_app.models import Bookmark
from buzzfire.bookmark_app.dao import BookmarkDao
from buzzfire.utils.utils import convert_to_builtin_type, check_auth, get_redis_conn

import simplejson as json

def add(request):
    oauth_status = check_auth(request)
    if oauth_status:
        conn = get_redis_conn()
        bookmark_dao = BookmarkDao(conn)
        if request.method == 'POST':
            owner_id = request.POST['owner_id']
            tweet_id = request.POST['tweet_id']
            tweet_txt = request.POST['tweet_txt']
            tweeter_screenname = request.POST['tweeter_screenname']
            if request.POST.has_key('latitude'):
                latitude = request.POST['latitude']
            else:
                latitude = None
            if request.POST.has_key('longitude'):
                longitude = request.POST['longitude']
            else:
                longitude =None
            bookmark = Bookmark(owner_id, tweet_id, tweet_txt, tweeter_screenname, location=(latitude, longitude))
            id = bookmark_dao.save(bookmark)
            
            if id:
                bookmark = bookmark_dao.get_bookmark(id)
                result = json.dumps(bookmark, default=Bookmark.json_encode)
                return HttpResponse(result)
            else:
                result ='{"status":"error"}'
                return HttpResponse(result)
        else:
            return HttpResponse()
    else:
        return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)
