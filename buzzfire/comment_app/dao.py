import datetime
from models import Comment

class CommentDao:
    def __init__(self, connection):
        self._connection = connection
        self._connection.setnx("comment:next_id", 1)

    def __validate(self, comment):
        if not hasattr(comment, "owner_id"):
            return False
        return True

    def save(self, comment):
        if self.__validate(comment):
            if not comment.id:
                comment.id = self._connection.get("comment:next_id")
                self._connection.incr("comment:next_id")
            self._connection.set("comment:%s:owner_id" %(comment.id), comment.owner_id)    
            self._connection.set("comment:%s:bookmark_id" %(comment.id), comment.bookmark_id)
            self._connection.set("comment:%s:text" %(comment.id), comment.text)
            self._connection.set("comment:%s:created" %(comment.id), comment.created.strftime("%Y-%m-%d %H:%M:%S"))
            self._connection.set("comment:%s:updated" %(comment.id), comment.updated.strftime("%Y-%m-%d %H:%M:%S"))
            self._connection.sadd("comment:members", comment.id)
            self._connection.rpush("user:%s:comments" %(comment.owner_id), comment.id)
            self._connection.rpush("bookmark:%s:comments" %(comment.bookmark_id), comment.id)
            
            return comment.id
        else:
            return None

    def delete(self, comment_id):
        self._connection.srem("comment:members", comment_id)
        owner_id = self._connection.get("comment:%s:owner_id" %(comment_id))
        bookmark_id = self._connection.get("comment:%s:bookmark_id" %(comment_id))
        self._connection.rpop("bookmark:%s:comments" %(bookmark_id), comment_id)
        self._connection.rpop("user:%s:comments" %(owner_id), comment_id)
        comment_keys = self._connection.keys("comment:%s:*" %(comment_id))
        if(len(comment_keys)!=0):
            for key in comment_keys:
                self._connection.delete(key)
            return True
        else:
            return False

    def delete_comment_user(self, user_id):
        comment_ids = self._connection.get("user:%s:comments" %(user_id))
        for comment_id in comment_ids:
            self.delete(comment_id)

    def get_owner_comment(self, owner_id):
        if self._connection.exists("user:%s:comments" %(owner_id)):
            owner_comment_ids = self._connection.lrange("user:%s:comments" %(owner_id),"0", self._connection.llen("user:%s:comments" %(owner_id)))
            owner_comments=[]
            for id in owner_comment_ids:
                comment = self.get_comment(id)
                owner_comments.append(comment)
            return owner_comments
        else:
            return []

    def get_bookmark_comment(self, bookmark_id):
        if self._connection.exists("bookmark:%s:comments" %(bookmark_id)):
            bookmark_comment_ids = self._connection.lrange("bookmark:%s:comments" %(bookmark_id), 0, self._connection.llen("bookmark:%s:comments" %(bookmark_id)))
            bookmark_comments=[]
            for id in bookmark_comment_ids:
                comment = self.get_comment(id)
                bookmark_comments.append(comment)
            return bookmark_comments
        else:
            return []

    def get_comment(self, id):
        bookmark_id = self._connection.get("comment:%s:bookmark_id" %(id))
        owner_id = self._connection.get("comment:%s:owner_id" %(id))
        text = self._connection.get("comment:%s:text" %(id))
        created = datetime.datetime.strptime(self._connection.get("comment:%s:created" %(id)),"%Y-%m-%d %H:%M:%S")
        updated = datetime.datetime.strptime(self._connection.get("comment:%s:updated" %(id)),"%Y-%m-%d %H:%M:%S")
        comment = Comment(id=id, owner_id=owner_id, bookmark_id=bookmark_id, text=text, created= created, updated = updated)
        return comment
