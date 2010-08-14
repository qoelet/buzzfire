import datetime

class Bookmark:
    def __init__(self,  owner_id, tweet_id, tweet_txt, tweeter_screenname, id=None, location=(None, None), created=datetime.datetime.now(), updated=datetime.datetime.now()):
        self.id = id
        self.owner_id=owner_id
        self.tweet_id = tweet_id
        self.tweet_txt = tweet_txt
        self.tweeter_screenname= tweeter_screenname
        self.location=location
        self.created = created
        self.updated = updated

class Tag:
    def __init__(self, text):
        self.text= text
