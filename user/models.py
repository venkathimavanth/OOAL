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
