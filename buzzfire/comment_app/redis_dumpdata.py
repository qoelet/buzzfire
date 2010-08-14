import simplejson as json
import redis

from models import Comment
from dao import CommentDao


def dumpdata():
    json_file = open('fixtures/fakers.json', 'r')
    json_string =''
    for line in json_file:
        json_string += line
    fake_data = json.loads(json_string)
    r = redis.Redis()
    owner_ids= []
    comment_ids =[]
    bookmark_ids =[]
    for faker in fake_data:
        owner_ids.append(faker['owner_id'])
        bookmark_ids.append(faker['bookmark_id'])
        comment = Comment(faker['owner_id'], faker['bookmark_id'], faker['text'])
        comment_dao = CommentDao(r)
        comment_id = comment_dao.save(comment)
        comment_ids.append(comment_id)
    
    test(comment_ids)
    test_comment_by_user(owner_ids)
    test_comment_by_bookmark(bookmark_ids)



def test(comment_ids):
    r = redis.Redis()
    comment_dao = CommentDao(r)
    
    for comment in comment_ids:
        got_comment =comment_dao.get_comment(comment)
        print convert_to_builtin_type(got_comment)

def test_comment_by_user(user_ids):
    r = redis.Redis()
    comment_dao = CommentDao(r)
    
    for user in user_ids:
        print "get comment for user %s" %(user)
        got_comment =comment_dao.get_owner_comment(user)
        print convert_to_builtin_type(got_comment)

def test_comment_by_bookmark(bookmark_ids):
    r = redis.Redis()
    comment_dao = CommentDao(r)
    
    for bookmark in bookmark_ids:
        print "get comment for bookmark %s" %(bookmark)
        got_comment =comment_dao.get_bookmark_comment(bookmark)
        print convert_to_builtin_type(got_comment)



def convert_to_builtin_type(obj):
        
        if(not isinstance(obj, (list, set))):
                obj = [obj]
        result=[]
        for o in obj:
                d = { 'type':o.__class__.__name__
                      }
                d.update(o.__dict__)
                result.append(d)
        
        return result

if __name__ == '__main__':
	dumpdata()
