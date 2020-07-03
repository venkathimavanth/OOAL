from mongoengine import connect,ObjectIdField,BooleanField,DateTimeField,StringField,IntField,ListField,ImageField,Document
from datetime import datetime

connect('EAD_OOAL')

class Message(Document):
    msg = StringField()
    sender = ObjectIdField()
    reciever = ObjectIdField()
    isRead = BooleanField(default=False)
    createdAt = DateTimeField(default=datetime.now())

class GroupMessage(Document):
    msg = StringField()
    sender = ObjectIdField()
    group = ObjectIdField()
    isRead = BooleanField(default=False)
    createdAt = DateTimeField(default=datetime.now())

