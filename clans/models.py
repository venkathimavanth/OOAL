from mongoengine import connect,ObjectIdField,DateTimeField,StringField,IntField,ListField,ImageField,Document
from datetime import datetime

connect('EAD_OOAL')

class community(Document):
    name=StringField(max_length=200)
    discription=StringField(max_length=200)
    no_of_participants = IntField(default=0)
    Heads = ListField(ObjectIdField())
    participants = ListField(ObjectIdField())
    group_challanges = ListField(ObjectIdField())
    messages = ListField(ObjectIdField())
    community_blog = ListField(ObjectIdField())
    photo = ImageField()
    createdAt = DateTimeField(default=datetime.now())


class Post(Document):
    description = StringField()
    image = ImageField()
    likes = IntField(default=0)
    likedBy = ListField(ObjectIdField())
    comments = ListField(ObjectIdField())
    reports = IntField(default=0)
    reportedBy = ListField(ObjectIdField())
    owner = ObjectIdField()
    createdAt = DateTimeField(default=datetime.now())

class Comment(Document):
    message = StringField()
    owner = ObjectIdField()
    reports = IntField(default=0)
    reportedBy = ListField(ObjectIdField())
