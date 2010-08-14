import datetime

class BookmarkDao:
    def __init__(self, connection):
        self._connection = connection
        self._connection.setnx("bookmark:next_id", 1)
    
    def __validate(self, bookmark):
        if not hasattr(bookmark, owner_id):
            return False
        if not hasattr(bookmark, tweet_id):
            return False
        if not hasattr(bookmark, tweet_txt):
            return False
        if not hasattr(bookmark, tweeter_screenname):
            return False
        return True

    def save(self, bookmark):
        if self.__validate(bookmark):
            if not bookmark.id:
                bookmark.id = self._connection.get("bookmark:next_id")
            self._connection.set("bookmark:%s:owner_id" %(bookmark.id), bookmark.owner_id)
            self._connection.set("bookmark:%s:tweet_id" %(bookmark.id), bookmark.tweet_id)
            self._connection.set("bookmark:%s:tweet_txt" %(bookmark.id), bookmark.tweet_txt)
            self._connection.set("bookmark:%s:tweeter_screenname" %(bookmark.id), bookmark.tweeter_screenname)
            self._connection.set("bookmark:%s:latitude" %(bookmark.id),  bookmark.location[0])
            self._connection.set("bookmark:%s:longitude" %(bookmark.id), bookmark.location[1])
                           
            self._connection.set("bookmark:%s:created" %(bookmark.id), bookmark.created.strftime("%Y-%m-%d %H:%M:%S"))
            self._connection.set("bookmark:%s:updated" %(bookmark.id), bookmark.updated.strftime("%Y-%m-%d %H:%M:%S"))
            self._connection.rpush("bookmark:bytime:bookmarks", bookmark.id)
            self._connection.rpush("user:%s:bookmarks" %(bookmark.owner_id), bookmarks)
            
            self._connection.zincrby("bookmark:byscore:bookmarks", bookmark.id, 0.0)
            self._connection.incr("bookmark:next_id")
            return bookmark.id
        else:
            return None
            
    def delete(self, bookmark_id):
        owner_id = self.__connection.get("bookmark:%s:owner_id" %bookmark_id)
        self._connection.spop("user:%s:bookmarks" %(owner_id), bookmark_id)
        if(self._connection.sismember("user:%s:likedbookmarks" %(owner_id), bookmark_id)):
            self.update_user_liked_bookmark(owner_id, -1)
        self._connection.zrem("bookmark:byscore:bookmarks", bookmark_id)
        self._connection.rpop("bookmark:bytime:bookmarks", bookmark_id)
        owner_id = self._connection.rpop("bookmark:%s:owner_id" %(bookmark_id))
        self._connection.rpop("user:%s:bookmarks" %(owner_id), bookmark_id)
        if(self._connection.exists("bookmark:%s:tags" %(bookmark_id))):
            tag_ids = self._connection.smembers("bookmark:%s:tags" %(bookmark_id))
            for id in tag_ids:
                self._connection.srem("tag:%s:bookmarks" %(id), bookmark_id)
        bookmark_keys = self._connection.keys("bookmark:%s:*" %(bookmark_id))
        if(len(bookmark_keys)):
            for key in bookmark_keys:
                self._connection.delete(key)
            return True
        else:
            return False
        
    def delete_bookmarks_user(self, user_id):
        user_bookmark_ids = self._connection.smembers("user:%s:bookmarks" %(user_id))
        for id in user_bookmark_ids:
            self.delete(key)
        

    def get_bookmark_of_user(self, user_id):
        if self._connection.exists("user:%s:bookmarks" %(user_id)):
            bookmark_ids = self._connection.smembers("user:%s:bookmarks" %(user_id)):
            bookmarks= []
            for id in bookmark_ids:
                bookmark = get_bookmark(id)
                bookmarks.append(bookmark)
        else:
            return []


    def get_bookmark(self, bookmark_id):
        owner_id = self._connection.get("bookmark:%s:owner_id" %(bookmark_id))
        tweet_id = self._connection.get("bookmark:%s:tweet_id" %(bookmark_id))
        tweet_txt = self._connection.get("bookmark:%s:tweet_txt" %(bookmark_id))
        tweeter_screenname = self._connection.get("bookmark:%s:tweeter_screenname" %(bookmark_id))
        location = (self._connection.get("bookmark:%s:latitude" %(bookmark_id), self._connection.get("bookmark:%s:longitude" %(bookmark_id))))
        created = datetime.datetime.strptime(self._connection.get("bookmark:%s:created" %(id)),"%Y-%m-%d %H:%M:%S")
        updated = datetime.datetime.strptime(self._connection.get("bookmark:%s:updated" %(id)),"%Y-%m-%d %H:%M:%S")
        bookmark = Bookmark(owner_id=owner_id, tweet_id=tweet_id, tweet_txt=tweet_txt, tweeter_screenname=tweeter_screenname, location=location, created=created, updated=updated, id=id)
        return bookmark
        
 

    def tag_bookmark(self, tag, bookmark_id):
        self._connection.sadd("tag:%s:bookmarks" %(tag), bookmark_id)
        self._connection.sadd("bookmark:%s:tags" %(bookmark_id), tag)


    def get_bookmark_by_tag(self, *tags):
        tag_keys=[]
        for tag in tags:
            tag_keys.append("tag:%s:bookmarks" %(tag))
        bookmark_key: = self._connection.sunion(tag_keys)
        for key in bookmark_key:
            self.get_bookmark(key)            

    def like_bookmark(self, user_id, bookmark_id):
        if not self._self._connection.sismember("bookmark:%s:likes" %(bookmark_id), user_id):
            # get total number of bookmark which user has
            total_bookmark_user = int(self._connection.llen("user:%s:bookmarks" %(user_id)))
            #get total number of bookmark which other user has like from this user
            total_liked_bookmark_of_user= int(self._connection.scard("user:%s:likedbookmarks" %(user_id)))
            # calculate the number of user like per bookmark
            score_of_user =float(total_liked_bookmark_of_user)/total_bookmark_user
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
            # calculate the new score of bookmark
            score_bookmark= new_total_score_bookmark/(total_num_user_like_bookmark+1)
            #update the total score of bookmark
            self._connection.set("bookmark:%s:totalscore" %(bookmark_id), new_total_score_bookmark)
            #update the user who like the bookmark
            self._connection.sadd("bookmark:%s:likes" %(bookmark_id), user_id)
            #get the owner who own the bookmark
            owner_id = self.connection.get("bookmark:%s:owner_id" %(bookmark_id))
            #add the bookmark to the list of bookmark of the owner which other ppl like
            self._connection.sadd("user:%s:likedbookmarks" bookmark_id)
            # update the score of the bookmark
            self._connection.zadd("bookmark:byscore:bookmarks", score_bookmark)
            
            #add one more bookmark to the bookmark that user like
            self._connection.sadd("user:%s:likes" %(user_id), bookmark_id)
            
            #update the score of the bookmarks of the owner of the bookmark who has just been liked.
            self.update_user_liked_bookmark(owner_id, 1)
            
            
    def update_user_liked_bookmark(self, user_id, amount):
        total_bookmark_user = int(self._connection.llen("user:%s:bookmarks" %(user_id)))
        total_liked_bookmark_of_user= int(self._connection.llen("user:%s:likedbookmarks" %(user_id)))
        old_score_of_user = float(total_liked_bookmark_of_user)/total_bookmark_user
        score_of_user =float(total_liked_bookmark_of_user+amount)/(total_bookmark_user)
        like_bookmark_of_user_ids = self._connection.smembers("user:%s:likes")
        for(id in like_bookmark_of_user_ids):
            self.update_bookmark_score(user_id, old_score_of_user, score_of_user, bookmark_id)


    def update_bookmark_score(self, user_id, old_score_of_user,user_new_score, bookmark_id):
        total_score_bookmark = float(self._connection.get("bookmark:%s:totalscore" %(bookmark_id)))
        total_num_user_like_bookmark = self._connection.scard("bookmark:%s:likes" %(bookmark_id))
        new_total_score_bookmark = total_score_bookmark - old_score_of_user +user_new_score
        score_bookmark= new_total_score_bookmark/(int(total_num_user_like_bookmark))
        self._connections.zadd("bookmark:byscore:bookmarks", score_bookmark)

    
    