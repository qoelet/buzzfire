import datetime

class Bookmark:
    def __init__(self,  owner_id, tweet_id, tweet_txt, tweeter_screenname, id=None, location=(None, None), created=datetime.datetime.now(), updated=datetime.datetime.now(), tags=[]):
        self.id = id
        self.owner_id=owner_id
        self.tweet_id = tweet_id
        self.tweet_txt = tweet_txt
        self.tweeter_screenname= tweeter_screenname
        self.location=location
        self.created = created
        self.updated = updated
        self.tags= tags

    def json_encode(obj):
        if isinstance(obj, Bookmark):
            tagstr="["
            for tag in obj.tags:
                tagstr= tagstr+"'"+tag+"',"
            if len(obj.tags)>=1:
                tagstr= tagstr[0:len(tagstr)-1]+"]"
            else:
                tagstr=tagstr+"]"
            return {"bookmark": {'id': obj.id, 'owner_id':obj.owner_id, 'tweet_id':obj.tweet_id, 'tweet_txt':obj.tweet_txt, 'tweeter_screenname':obj.tweeter_screenname, 'location.latitude':obj.location[0], 'location.longitude':obj.location[1], 'created':obj.created.strftime('%Y-%m-%dT%H:%M:%S'), 'updated':obj.updated.strftime('%Y-%m-%dT%H:%M:%S'), 'tags': obj.tags}} 
        else:
            return {}

class Tag:
    def __init__(self, text):
        self.text= text
