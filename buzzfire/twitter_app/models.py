class User:
    def __init__(self, screenname, twitter_id, id=None, oauth_token_secret=None, oauth_token=None, location=(None, None)):
        self.id = id
        self.screenname=screenname
        self.twitter_id = twitter_id
        self.oauth_token_secret=oauth_token_secret
        self.oauth_token = oauth_token
        self.location = location