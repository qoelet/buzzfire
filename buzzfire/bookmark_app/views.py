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
            owner_id = request.session['buzz_user_id']
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
                return HttpResponse(result, content_type = "application/json")
            else:
                result ='{"status":"error"}'
                return HttpResponse(result)
        else:
            return HttpResponse()
    else:
        return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)

def get_user_bookmark(request, user_id=None):
    oauth_status = check_auth(request)
    if oauth_status:
	
		if user_id == None:
			user_id = request.session['buzz_user_id']
			
        conn = get_redis_conn()
        bookmark_dao = BookmarkDao(conn)
        if request.method =='GET':
            if request.GET.has_key("offset"):
                offset = request.GET['offset']
            else:
                offset = 0
            if request.GET.has_key("length"):
                length = str(int(request.GET['length'])-1)
            else:
                length ='-1'
            bookmarks = bookmark_dao.get_bookmark_of_user(user_id, offset, length)
            result  = json.dumps(bookmarks, default=Bookmark.json_encode)
            return HttpResponse(result, content_type = "application/json")
        else:
            return HttpResponse()
    else:
        return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)

def tag_bookmark(request, bookmark_id):
    oauth_status = check_auth(request)
    if oauth_status:
        conn = get_redis_conn()
        bookmark_dao = BookmarkDao(conn)
        if request.method == 'POST':
            tag = request.POST['tag']
            bookmark_dao.tag_bookmark(tag, bookmark_id)
            return HttpResponse(tag, content_type = "application/json")
        else:
            return HttpResponse()
    else:
        return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)
    
def untag_bookmark(request, bookmark_id):
    oauth_status = check_auth(request)
    if oauth_status:
        conn = get_redis_conn()
        bookmark_dao = BookmarkDao(conn)
        if request.method == 'POST':
            tag = request.POST['tag']
            bookmark_dao.untag_bookmark(tag, bookmark_id)
            return HttpResponse(tag, content_type = "application/json")
        else:
            return HttpResponse()
    else:
        return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)
    
def delete_bookmark(request, bookmark_id):
    oauth_status = check_auth(request)
    if oauth_status:
        conn = get_redis_conn()
        bookmark_dao = BookmarkDao(conn)
        if request.method == 'POST':
            status = bookmark_dao.delete(bookmark_id)
            if status:
                  return HttpResponse('{"status":"Success"}', content_type = "application/json")
            else:
                return HttpResponse('{"status":"Error"}', content_type = "application/json")
        else:
            return HttpResponse()
    else:
        return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)
            

def like_bookmark(request, bookmark_id):
    oauth_status = check_auth(request)
    if oauth_status:
        conn = get_redis_conn()
        bookmark_dao = BookmarkDao(conn)
        if request.method == 'POST':
            user_id = request.session['buzz_user_id']
            bookmark_dao.like_bookmark(user_id, bookmark_id)
            return HttpResponse(bookmark_id, content_type="application/json")
        else:
            return HttpResponse()
    else:
        return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)


def get_bookmark_by_rank(request):
    oauth_status = check_auth(request)
    if oauth_status:
        conn = get_redis_conn()
        bookmark_dao = BookmarkDao(conn)
        if request.method =='GET':
            if request.GET.has_key("offset"):
                offset = request.GET['offset']
            else:
                offset = 0
            if request.GET.has_key("length"):
                length = str(int(request.GET['length'])-1)
            else:
                length ='-1'

            bookmarks = bookmark_dao.get_bookmark_by_rank(offset, length)
            result  = json.dumps(bookmarks, default=Bookmark.json_encode)
            return HttpResponse(result, content_type = "application/json")
        else:
            return HttpResponse()
    else:
        return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)

            
def get_user_bookmark_by_rank(request, user_id):
    oauth_status = check_auth(request)
    if oauth_status:
        conn = get_redis_conn()
        bookmark_dao = BookmarkDao(conn)
        if request.method =='GET':
            if request.GET.has_key("offset"):
                offset = request.GET['offset']
            else:
                offset = 0
            if request.GET.has_key("length"):
                length = str(int(request.GET['length'])-1)
            else:
                length ='-1'

            bookmarks = bookmark_dao.get_user_bookmark_by_rank(user_id, offset, length)
            result  = json.dumps(bookmarks, default=Bookmark.json_encode)
            return HttpResponse(result, content_type = "application/json")
        else:
            return HttpResponse()
    else:
        return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)


def get_user_bookmark_rank(request, bookmark_id):
    oauth_status = check_auth(request)
    if oauth_status:
        conn = get_redis_conn()
        bookmark_dao = BookmarkDao(conn)
        if request.method =='GET':
            user_id =request.session['buzz_user_id']
            rank = bookmark_dao.get_bookmark_user_rank(user_id, bookmark_id)
            if rank:
                return HttpResponse(rank, content_type = "application/json")
            else:
                return HttpResponse("{'status':'error'}", content_type="application/json")
        else:
            return HttpResponse()
    else:
        return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)

def get_global_bookmark_rank(request, bookmark_id):
    
    oauth_status = check_auth(request)
    if oauth_status:
        conn = get_redis_conn()
        bookmark_dao = BookmarkDao(conn)
       
        if request.method =='GET':
           
            rank = bookmark_dao.get_bookmark_global_rank(bookmark_id)
        
            if rank:
                return HttpResponse(rank, content_type = "application/json")
            else:
                return HttpResponse("{'status':'error'}", content_type="application/json")
        else:
            return HttpResponse()
    else:
        return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)

def get_bookmark_by_time(request):
    oauth_status = check_auth(request)
    if oauth_status:
        conn = get_redis_conn()
        bookmark_dao = BookmarkDao(conn)
        if request.method =='GET':
            if request.GET.has_key("offset"):
                offset = request.GET['offset']
            else:
                offset = 0
            if request.GET.has_key("length"):
                length = str(int(request.GET['length'])-1)
            else:
                length ='-1'

            bookmarks = bookmark_dao.get_bookmark_by_time(offset, length)
            result  = json.dumps(bookmarks, default=Bookmark.json_encode)
            return HttpResponse(result, content_type = "application/json")
        else:
            return HttpResponse()
    else:
        return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)

