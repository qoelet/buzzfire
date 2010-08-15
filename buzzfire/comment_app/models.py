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
            return {"user":r"{'id':'%s', 'owner_id':'%s', 'bookmark_id':'%s', 'text':'%s', 'created':'%s', 'updated':'%s'}" %(obj.id, obj.owner_id, obj.bookmark_id, obj.text, obj.created.strftime('%Y-%m-%dT%H:%M:%S'), obj.updated.strftime('%Y-%m-%dT%H:%M:%S'))}
        else:
            return {}
        
