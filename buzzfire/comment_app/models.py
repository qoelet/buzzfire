import datetime

class Comment:
    def __init__(self, owner_id, bookmark_id, text="", id=None, created=datetime.datetime.now(), updated=datetime.datetime.now()):
        self.id = id
        self.owner_id=owner_id
        self.bookmark_id = bookmark_id
        self.text=text
        self.created=created
        self.updated=updated
        
