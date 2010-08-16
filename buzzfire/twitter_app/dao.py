from models import User

class UserDao:
    def __init__(self, connection):
        self._connection = connection
        self._connection.setnx("user:next_id", 1)

    def validate(self, user):
        if not hasattr(user, "screenname"):
            return False
        if not hasattr(user, "twitter_id"):
            return False
        return True

    def save(self, user):
        pipeline = self._connection.pipeline()
        if self.validate(user):
            if not user.id:
                user.id = self._connection.get("user:next_id")
                self._connection.incr("user:next_id")
            lock = self._connection.lock("lock")
            user_lock = self._connection.lock("user:%s" %(user.id))
            
            lock.acquire()
            user_lock.acquire()
            lock.release()
            try:
                pipeline.set("user:%s:id" %(user.screenname), user.id) 
                pipeline.set("user:%s:screenname" %(user.id), user.screenname)
                pipeline.set("user:%s:twitter_id" %(user.id), user.twitter_id)
                pipeline.set("user:%s:oauth_token" %(user.id), user.oauth_token)
                pipeline.set("user:%s:oauth_token_secret" %(user.id), user.oauth_token_secret)
                pipeline.set("user:%s:longitude" %(user.id), user.location[1])
                pipeline.set("user:%s:latitude" %(user.id), user.location[0])
                pipeline.sadd("user:members", user.id)
                pipeline.execute()
                return user.id
            finally:
                user_lock.release()
        else:
            return None
    
    def delete(self, user_id):
        pipeline = self._connection.pipeline()
        lock = self._connection.lock("lock")
        user_lock = self._connection.lock("user:%s" %(user_id))
        lock.acquire()
        user_lock.acquire()
        lock.release()
        try:
            pipeline..srem("user:members", user_id)
            user_keys = self._connection.keys("user:%s:*" %(user_id))
            if(len(user_keys)!=0):
                for key in user_keys:
                    pipeline.delete(key)
            pipeline.execute()
            return True
        finally:
            user_lock.release()

        
        
            
    def get_user(self, id):
        pipeline = self._connection.pipeline()
        screenname = pipeline.get("user:%s:screenname" %(id))
        twitter_id = pipeline.get("user:%s:twitter_id" %(id))
        oauth_token_secret = pipeline.get("user:%s:oauth_token_secret" %(id))
        oauth_token = pipeline.get("user:%s:oauth_token" %(id))
        pipeline.get("user:%s:latitude" %(id))
        pipeline.get("user:%s:longitude" %(id))
        screenname, twitter_id, oauth_token_secret, oauth_token, latitude, longitude =pipeline.execute()
        location = (latitude, longitude)
        user = User(id=id, screenname=screenname, twitter_id=twitter_id, oauth_token_secret = oauth_token_secret, oauth_token=oauth_token, location=location)
        return user
        
    def get_user_id(self, screenname):
        if self._connection.exists("user:%s:id" %(screenname)):
            return self._connection.get("user:%s:id" %(screenname))
        else:
            return None


            



                    
        
