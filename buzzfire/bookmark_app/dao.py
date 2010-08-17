import datetime
from models import Bookmark

class BookmarkDao:
    def __init__(self, connection):
        self._connection = connection
        self._connection.setnx("bookmark:next_id", 1)
    
    def __validate(self, bookmark):
        if not hasattr(bookmark, "owner_id"):
            return False
        if not hasattr(bookmark, "tweet_id"):
            return False
        if not hasattr(bookmark, "tweet_txt"):
            return False
        if not hasattr(bookmark, "tweeter_screenname"):
            return False
        return True

    def save(self, bookmark):
        if self.__validate(bookmark):
            pipeline = self._connection.pipeline()
            if not bookmark.id:
                bookmark.id = self._connection.get("bookmark:next_id")
                self._connection.incr("bookmark:next_id")

            if(not self._connection.sismember("user:%s:bookmark_set_tweet_ids" %(bookmark.owner_id), bookmark.tweet_id)):
                lock = self._connection.lock("lock")
                user_lock = self._connection.lock("user:%s" %(bookmark.owner_id))
                bookmark_lock = self._connection.lock("bookmark:%s" %(bookmark.id))
                lock.acquire()
                user_lock.acquire()
                bookmark_lock.acquire()
                lock.release()
                try:
                    pipeline.set("bookmark:%s:owner_id" %(bookmark.id), bookmark.owner_id)
                    pipeline.set("bookmark:%s:tweet_id" %(bookmark.id), bookmark.tweet_id)
                    pipeline.set("bookmark:%s:tweet_txt" %(bookmark.id), bookmark.tweet_txt)
                    pipeline.set("bookmark:%s:tweeter_screenname" %(bookmark.id), bookmark.tweeter_screenname)
                    pipeline.set("bookmark:%s:latitude" %(bookmark.id),  bookmark.location[0])
                    pipeline.set("bookmark:%s:longitude" %(bookmark.id), bookmark.location[1])
                           
                    pipeline.set("bookmark:%s:created" %(bookmark.id), bookmark.created.strftime("%Y-%m-%d %H:%M:%S"))
                    pipeline.set("bookmark:%s:updated" %(bookmark.id), bookmark.updated.strftime("%Y-%m-%d %H:%M:%S"))
                    pipeline.lpush("bookmark:bytime:bookmarks", bookmark.id)
                    pipeline.incr("user:%s:%s:total_bookmarks" %(bookmark.owner_id, bookmark.created.strftime("%Y-%m")))
                    pipeline.lpush("user:%s:bookmarks" %(bookmark.owner_id), bookmark.id)
                    pipeline.sadd("user:%s:bookmarks_set" %(bookmark.owner_id), bookmark.id)
                    pipeline.sadd("user:%s:bookmark_set_tweet_ids" %(bookmark.owner_id), bookmark.tweet_id)
                    pipeline.zincrby("bookmark:byscore:bookmarks", bookmark.id, 0.0)
                    pipeline.zincrby("user:%s:byscore:bookmarks" %(bookmark.owner_id), bookmark.id, 0.0)
                    pipeline.execute()
                    
                    
                    return bookmark.id
                finally:
                    bookmark_lock.release()
                    user_lock.release()

            else:
                return None
        else:
            return None
            
    def delete(self, bookmark_id):
        
        pipeline = self._connection.pipeline()
        owner_id = self._connection.get("bookmark:%s:owner_id" %bookmark_id)
        
        lock = self._connection.lock("lock")
        bookmark_lock = self._connection.lock("bookmark:%s" %(bookmark_id))
        user_lock = self._connection.lock("user:%s" %(owner_id))
        
        lock.acquire()
        bookmark_lock.acquire()
        user_lock.acquire()
        lock.release()
        
        try:
            pipeline.lrem("user:%s:bookmarks" %(owner_id), bookmark_id)
            pipeline.zrem("user:%s:byscore:bookmarks" %(owner_id), bookmark_id)
            #if(pipeline.sismember("user:%s:likedbookmarks" %(owner_id), bookmark_id)):
             #    self.update_user_liked_bookmark(owner_id, -1)
            pipeline.zrem("bookmark:byscore:bookmarks", bookmark_id)
            pipeline.lrem("bookmark:bytime:bookmarks", bookmark_id)
            pipeline.lrem("user:%s:bookmarks" %(owner_id), bookmark_id)
            pipeline.srem("user:%s:bookmarks_set" %(owner_id), bookmark_id)
            pipeline.srem("user:%s:bookmark_set_tweet_ids" %(owner_id), pipeline.get("bookmark:%s:tweet_id" %(bookmark_id)))
            if(self._connection.exists("bookmark:%s:tags" %(bookmark_id))):
                tag_ids = self._connection.smembers("bookmark:%s:tags" %(bookmark_id))
                for id in tag_ids:
                    pipeline.srem("tag:%s:bookmarks" %(id), bookmark_id)
            bookmark_keys = self._connection.keys("bookmark:%s:*" %(bookmark_id))
            if(len(bookmark_keys)):
                for key in bookmark_keys:
                    pipeline.delete(key)
            pipeline.execute()
            
            
            return True
        finally:
            bookmark_lock.release()
            user_lock.release()
        


    #cannot lock owner here because delete also is trying to get owner lock, wait get deadlock
    def delete_bookmarks_user(self, user_id):
        if self._connection.exists("user:%s:bookmarks" %(user_id)):
            user_bookmark_ids = self._connection.smembers("user:%s:bookmarks" %(user_id))
            for id in user_bookmark_ids:
                self.delete(key)
        

    def get_bookmark_of_user(self, user_id, offset='0', length='-1'):
        if self._connection.exists("user:%s:bookmarks" %(user_id)):
            if int(length)<=-1:
                length = self._connection.llen("user:%s:bookmarks" %(user_id))
        
        
            bookmark_ids = self._connection.lrange("user:%s:bookmarks" %(user_id), str(offset), str(int(offset)+int(length)))
            bookmarks= []
            for id in bookmark_ids:
                bookmark = self.get_bookmark(id)
                bookmarks.append(bookmark)
            return bookmarks
        else:
            return []


    def get_bookmark(self, bookmark_id):
        pipeline = self._connection.pipeline()
        pipeline.get("bookmark:%s:owner_id" %(bookmark_id))
        pipeline.get("bookmark:%s:tweet_id" %(bookmark_id))
        pipeline.get("bookmark:%s:tweet_txt" %(bookmark_id))
        pipeline.get("bookmark:%s:tweeter_screenname" %(bookmark_id))
        pipeline.get("bookmark:%s:latitude" %(bookmark_id)) 
        pipeline.get("bookmark:%s:longitude" %(bookmark_id))
        pipeline.get("bookmark:%s:created" %(bookmark_id))
        pipeline.get("bookmark:%s:updated" %(bookmark_id))
        if self._connection.exists("bookmark:%s:tags" %(bookmark_id)):
            tags = pipeline.smembers("bookmark:%s:tags" %(bookmark_id))
            owner_id, tweet_id, tweet_txt, tweeter_screenname, latitude, longitude, created, updated, tags = pipeline.execute()
            created =   datetime.datetime.strptime(created,"%Y-%m-%d %H:%M:%S")
            updated =   datetime.datetime.strptime(updated,"%Y-%m-%d %H:%M:%S")
            location=(latitude, longitude)
        else:
            tags = set()
            owner_id, tweet_id, tweet_txt, tweeter_screenname, latitude, longitude, created, updated = pipeline.execute()
            location=(latitude, longitude)
            created =   datetime.datetime.strptime(created,"%Y-%m-%d %H:%M:%S")
            updated =   datetime.datetime.strptime(updated,"%Y-%m-%d %H:%M:%S")
       
        
        bookmark = Bookmark(owner_id=owner_id, tweet_id=tweet_id, tweet_txt=tweet_txt, tweeter_screenname=tweeter_screenname, location=location, created=created, updated=updated, id=bookmark_id, tags=list(tags))
        return bookmark
        
 

    def tag_bookmark(self, tag, bookmark_id):
        pipline = self._connection.pipeline()
        pipeline.sadd("tag:%s:bookmarks" %(tag), bookmark_id)
        pipeline.sadd("bookmark:%s:tags" %(bookmark_id), tag)
        pipeline.sadd("tag:members", tag)
        pipeline.execute()

    def untag_bookmark(self, tag, bookmark_id):
        pipline = self._connection.pipeline()
        pipeline.srem("tag:%s:bookmarks" %(tag), bookmark_id)
        pipeline.srem("bookmark:%s:tags" %(bookmark_id), tag)
        pipeline.execute()

    def get_bookmark_by_tag(self, *tags):
        tag_keys=[]
        for tag in tags:
            tag_keys.append("tag:%s:bookmarks" %(tag))
        bookmark_key = self._connection.sunion(tag_keys)
        bookmarks = []
        for key in bookmark_key:
            bookmarks.append(self.get_bookmark(key))
        return bookmarks

    def like_bookmark(self, user_id, bookmark_id):
        pipeline = self._connection.pipeline()
        if not self._connection.sismember("bookmark:%s:likes" %(bookmark_id), user_id) and not self._connection.sismember("user:%s:bookmark_set" %(user_id), bookmark_id):
            
            #get the owner who own the bookmark
            owner_id = self._connection.get("bookmark:%s:owner_id" %(bookmark_id))
            
            owner_lock = self._connection.lock("user:%s" %(owner_id))
            user_lock = self._connection.lock("user:%s" %(user_id))
            bookmark_lock = self._connection.lock("bookmark:%s" %(bookmark_id))
            lock = self._connection.lock("lock")
            
            lock.acquire()
            owner_lock.acquire()
            user_lock.acquire()
            bookmark_lock.acquire()
            lock.release()
            
            try:
         
                # get total number of bookmark which user in this month
                current_month = datetime.datetime.now()
                if (self._connection.exists("user:%s:%s:total_bookmarks" %(user_id, current_month.strftime("%Y-%m")))):
                    total_bookmark_user= int(self._connection.get("user:%s:%s:total_bookmarks" %(user_id, current_month.strftime("%Y-%m"))))
                else:
                    total_bookmark_user = 0.0

                #get total number of bookmark which other user has like from this user in this month
                if(self._connection.exists("user:%s:%s:total_bookmarks_like_by_others" %(user_id, current_month.strftime("%Y-%m")))):
                    total_liked_bookmark_of_user= int(self._connection.get("user:%s:%s:total_bookmarks_like_by_others" %(user_id, current_month.strftime("%Y-%m"))))
                else:
                    total_liked_bookmark_of_user =0
                
                # calculate the number of user like per bookmark
                if total_bookmark_user!=0:
                    score_of_user =float(total_liked_bookmark_of_user)/total_bookmark_user 
                    #print score_of_user
                else:
                    score_of_user =0.0
                
                #get the totalscore of the bookmark
                if self._connection.exists("bookmark:%s:totalscore" %(bookmark_id)):
                    total_score_bookmark = float(self._connection.get("bookmark:%s:totalscore" %(bookmark_id)))
                else:
                    total_score_bookmark = 0.0
            
                #get the number of ppl that like the bookmark
                if self._connection.exists("bookmark:%s:likes" %(bookmark_id)):
                    total_num_user_like_bookmark = self._connection.scard("bookmark:%s:likes" %(bookmark_id))
                else:
                    total_num_user_like_bookmark = 0.0
            
                # calculate the new total score of bookmark
                new_total_score_bookmark = score_of_user + total_score_bookmark
                #total number of user in the system
                total_user = float(self._connection.scard("user:members"))
                # calculate the new score of bookmark
                score_bookmark= (new_total_score_bookmark/(total_num_user_like_bookmark+1))/total_user
                #print score_bookmark
                #update the total score of bookmark
                pipeline.set("bookmark:%s:totalscore" %(bookmark_id), new_total_score_bookmark)

                #update the user who like the bookmark
                pipeline.sadd("bookmark:%s:likes" %(bookmark_id), user_id)


                #update the total bookmark like by the user in this month by 1
                pipeline.incr("user:%s:%s:total_bookmarks_like_by_others" %(owner_id, current_month.strftime("%Y-%m")))

                #add the bookmark to the list of bookmark of the owner which other ppl like
                pipeline.sadd("user:%s:likedbookmarks" %(owner_id), bookmark_id)
                
                # update the score of the bookmark
            
                pipeline.zadd("bookmark:byscre:bookmarks", bookmark_id, score_bookmark)
                pipeline.zadd("user:%s:byscore:bookmarks" %(owner_id), bookmark_id, score_bookmark)
                #add one more bookmark to the bookmark that user like
                pipeline.sadd("user:%s:likes" %(user_id), bookmark_id)
                pipeline.execute()
            
            finally:
                owner_lock.release()
                bookmark_lock.release()
                user_lock.release()


    def get_bookmark_by_rank(self, offset='0', length='-1'):
        if int(length)<0:
            length = self._connection.zcard("bookmark:byscore:bookmarks")
            
        bookmark_ids = self._connection.zrevrange("bookmark:byscore:bookmarks", offset, str(int(offset)+int(length)))
        bookmarks=[]
        if bookmark_ids:
            for id in bookmark_ids:
                bookmarks.append(self.get_bookmark(id))
        return bookmarks

    def get_user_bookmark_by_rank(self, user_id, offset='0', length='-1'):
        if int(length)<0:
            length = self._connection.zcard("user:%s:byscore:bookmarks", user_id)
            
        bookmark_ids = self._connection.zrevrange("user:%s:byscore:bookmarks" %(user_id), offset, str(int(offset)+int(length)))
        
        bookmarks=[]
        if (bookmark_ids):
            for id in bookmark_ids:
                bookmarks.append(self.get_bookmark(id))
        return bookmarks
                                              
    
    def get_bookmark_global_rank(self, bookmark_id):
        rank = self._connection.zrank("bookmark:byscore:bookmarks", bookmark_id)
        return rank

    def get_bookmark_user_rank(self, user_id, bookmark_id):
        rank = self._connection.zrank("user:%s:byscore:bookmarks" %(user_id), bookmark_id)
        return rank

    def get_bookmark_by_time(self, offset='0', length='-1'):
        if int(length)<0:
            length = self._connection.llen("bookmark:bytime:bookmarks")
       
        
        bookmark_ids = self._connection.lrange("bookmark:bytime:bookmarks", offset, str(int(offset)+int(length)))
        bookmarks=[]
        if(bookmark_ids):
            for id in bookmark_ids:
                bookmarks.append(self.get_bookmark(id))
        return bookmarks

    def get_users_who_like_bookmark(self, bookmark_id):
        if self._connection.exists("bookmark:%s:likes" %(bookmark_id)):
            user_ids = self._connection.smembers("bookmark:%s:likes" %(bookmark_id))
            users =[]
            for user_id in user_ids:
                users.append(self._connection.get("user:%s:screenname" %(user_id)))
            return users
        else:
            return []
            
            #self.update_user_liked_bookmark(owner_id, 1)
            
'''            
    def update_user_liked_bookmark(self, user_id, amount):
        total_bookmark_user = int(self._connection.llen("user:%s:bookmarks" %(user_id)))
        total_liked_bookmark_of_user= int(self._connection.llen("user:%s:likedbookmarks" %(user_id)))
        old_score_of_user = float(total_liked_bookmark_of_user)/total_bookmark_user
        score_of_user =float(total_liked_bookmark_of_user+amount)/(total_bookmark_user)
        if self._connection.exists("user:%s:likes" %(user_id)):
            like_bookmark_of_user_ids = self._connection.smembers("user:%s:likes" %(user_id))
            for id in like_bookmark_of_user_ids:
                self.update_bookmark_score(user_id, old_score_of_user, score_of_user, bookmark_id)


    def update_bookmark_score(self, user_id, old_score_of_user,user_new_score, bookmark_id):
        total_score_bookmark = float(self._connection.get("bookmark:%s:totalscore" %(bookmark_id)))
        total_num_user_like_bookmark = self._connection.scard("bookmark:%s:likes" %(bookmark_id))
        new_total_score_bookmark = total_score_bookmark - old_score_of_user +user_new_score
        score_bookmark= new_total_score_bookmark/(int(total_num_user_like_bookmark))
        self._connections.zadd("bookmark:byscore:bookmarks", score_bookmark)
'''
