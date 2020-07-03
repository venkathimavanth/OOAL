from mongoengine import connect,ObjectIdField,BooleanField,DateTimeField,StringField,IntField,ListField,ImageField,Document
from datetime import datetime

DB_URI = "mongodb+srv://ead118:myclan#2@ead.epyex.mongodb.net/EAD?retryWrites=true&w=majority"
connect(host=DB_URI)

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
