from mongoengine import connect,ObjectIdField,StringField,IntField,ListField,ImageField,DateTimeField, BooleanField, Document,FileField

connect("EAD_OOAL")




class Post(Document):
    user_id =  ObjectIdField()
    user_photo = ImageField()
    created_date=DateTimeField()
    reports=ListField(ObjectIdField())

    isimage = BooleanField(default=False)
    isvideo = BooleanField(default=False)

    text = StringField(max_length=200)
    content =  FileField()

    ischallenge = BooleanField(default=False)
    challegetype=StringField(max_length=200)
    challengeid=ObjectIdField()

    isad=BooleanField(default=False)
    adid=ObjectIdField()

    likes=ListField(ObjectIdField())
    comments=ListField(ObjectIdField())

class Comment(Document):
    message = StringField()
    owner = ObjectIdField()
    reports = IntField(default=0)
    reportedBy = ListField(ObjectIdField())


class FriendToFriend(Document):
    user_id =  ObjectIdField()
    created_date=DateTimeField()
    age_restricted=BooleanField(default=False)
    name = StringField(max_length=200)
    discription = StringField(max_length=1000)
