from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.http import Http404

from buzzfire.comment_app.models import Comment
from buzzfire.comment_app.dao import CommentDao
from buzzfire.utils.utils import convert_to_builtin_type, check_auth, get_redis_conn

import simplejson as json

def add(request):
    oauth_status = check_auth(request)
    if oauth_status:
        conn = get_redis_conn()
        comment_dao = CommentDao(conn)
        if request.method  == 'POST':
            owner_id = request.POST["owner_id"]
            bookmark_id = request.POST["bookmark_id"]
            text = request.POST["text"]
            comment = Comment(owner_id, bookmark_id, text)
            id = comment_dao.save(comment)
            if id:
                comment = comment_dao.get_comment(id)
                result  = json.dumps(comment, default=Comment.json_encode)
                return HttpResponse(result)
            else:
                result = '{"status":"error"}'
                return HttpResponse(result)
        else:
            return HttpResponse()
    else:
        return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)


def get_bookmark_comment(request, bookmark_id):
    oauth_status = check_auth(request)
    if oauth_status:
        conn = get_redis_conn()
        comment_dao = CommentDao(conn)
        if request.method =='GET':
            comments = comment_dao.get_bookmark_comment(bookmark_id)
            result  = json.dumps(comments, default=Comment.json_encode)
            return HttpResponse(result)
        else:
            return HttpResponse()
    else:
        return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)


def get(request, comment_id):
    oauth_status = check_auth(request)
    if oauth_status:
        conn = get_redis_conn()
        comment_dao = CommentDao(conn)
        if request.method =='GET':
            comment = comment_dao.get_comment(comment_id)
            if comment:
                result  = json.dumps(comment, default=Comment.json_encode)
                return HttpResponse(result)
            else:
                return Http404
    else:
        return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)
    

def delete(request, comment_id):
    oauth_status = check_auth(request)
    if oauth_status:
        conn = get_redis_conn()
        comment_dao = CommentDao(conn)
        if request.method =='POST':
            status = comment_dao.delete(id)
            if status:
                return HttpResponse('{"status":"Success"}')
            else:
                return HttpResponse('{"status":"Error"}')
        else:
            return HttpResponse()
    else:
        return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)

    
        

              
            
            
            
            
            

        
        
        
