import datetime

class Comment:
    def __init__(self, owner_id, bookmark_id, text="", id=None, created=datetime.datetime.now(), updated=datetime.datetime.now()):
        self.id = id
        self.owner_id=owner_id
        self.bookmark_id = bookmark_id
        self.text=text
        self.created=created
        self.updated=updated
        
    def json_encode(obj):
        if isinstance(obj, Comment):
            return {"user":{'id':obj.id, 'owner_id':obj.owner_id, 'bookmark_id':obj.bookmark_id, 'text':obj.text, 'created':obj.created.strftime('%Y-%m-%dT%H:%M:%S'), 'updated': obj.updated.strftime('%Y-%m-%dT%H:%M:%S')}} 
        else:
            return {}
        
