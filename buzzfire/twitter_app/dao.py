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
        if self.validate(user):
            if not user.id:
                user.id = self._connection.get("user:next_id")
            self._connection.set("user:%s:id" %(user.screenname), user.id) 
            self._connection.set("user:%s:twitter_id" %(user.id), user.twitter_id)
            self._connection.set("user:%s:oauth_token" %(user.id), user.oauth_token)
            self._connection.set("user:%s:ouath_token_secret" %(user.id), user.oauth_token_secret)
            self._connection.set("user:%s:longitude" %(user.id), user.location[1])
            self._connection.set("user:%s:latitude" %(user.id), user.location[0])
            self._connection.sadd("user:members", user.id)
            self._connection.incr("user:next_id")
            return user.id
        else:
            return None
    
    def delete(self, user_id):
        self._connection.srem("user:members", user_id)
        user_keys = self._connection.keys("user:%s:*" %(user_id)).split()
        if(len(user_keys)!=0):
            for key in user_keys:
                self._connection.delete(key)
            return True
        else:
            return False
        
        
    def get_user(self, id):
        screenname = self._connection.get("user:%s:screenname" %(id))
        twitter_id = self._connection.get("user:%s:twitter_id" %(id))
        oauth_token_secret = self._connection.get("user:%s:oauth_token_secret" %(id))
        oauth_token = self._connection.get("user:%s:oauth_token" %(id))
        location = (self._connection.get("user:%s:latitude" %(id)), self._connection.get("user:%s:longitude" %(id)))
        user = User(id=id, screenname=screenname, twitter_id=twitter_id, oauth_token_secret = oauth_token_secret, oauth_token=oauth_token, location=location)
        return user
        
    def get_user_id(self, screenname):
        if self._connection.exists("user:%s:id" %(screenname)):
            return self._connection.get("user:%s:id" %(screenname))
        else:
            return None


            



                    
        
