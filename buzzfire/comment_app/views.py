from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.http import Http404

from buzzfire.comment_app.models import Comment
from buzzfire.comment_app.dao import Comment
from buzzfire.utils.utils import convert_to_builtin_type, check_auth, get_redis_conn

import json

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
            id = commentDao.save(comment)
            if id:
                comment = commentDao.get_comment(id)
                result  = json.dumps(convert_to_builtin_type(comment))
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
        comment_dao = CommentDao(conn):
        if request.method =='GET':
            comments = comment_dao.get_bookmark_comment(bookmark_id)
            result = json.dumps(convert_to_builtin_type(comments))
            return HttpResponse(result)
        else:
            return HttpResponse()
    else:
        return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)


def get(request, comment_id):
    oauth_status = check_auth(request)
    if oauth_status:
        conn = get_redis_conn()
        comment_dao = CommentDao(conn):
        if request.method =='GET':
            comment = commentDao.get_comment(id)
            if comment:
                result  = json.dumps(convert_to_builtin_type(comment))
                return HttpResponse(result)
            else:
                return Http404
    else:
        return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)
    

def delete(request, comment_id):
    oauth_status = check_auth(request)
    if oauth_status:
        conn = get_redis_conn()
        comment_dao = CommentDao(conn):
        if request.method =='POST':
            status = commentDao.delete(id)
            if status:
                return HttpResponse('{"status":"Success"}')
            else:
                return HttpResponse('{"status":"Error"}')
        else:
            return HttpResponse()
    else:
        return HttpResponseRedirect(settings.BUZZFIRE_LOGIN_URL)

    
        

    
              
            
            
            
            
            

        
        
        
