from mongoengine import connect,ObjectIdField,StringField,IntField,ListField,ImageField,DateTimeField, BooleanField, Document

connect("EAD_OOAL")




class Post(Document):
    user_id =  ObjectIdField(unique = True)
    user_photo = ImageField()
    created_date=DateTimeField()
    reports=ListField(ObjectIdField())

    istext = BooleanField(default=False)
    isimage = BooleanField(default=False)
    isvideo = BooleanField(default=False)

    text = StringField(max_length=200)
    image = ImageField()
    text = StringField(max_length=200)

    ischallenge = BooleanField(default=False)
    challegetype=StringField(max_length=200)
    challengeid=ObjectIdField()

    isad=BooleanField(default=False)
    adid=ObjectIdField()

    likes=ListField(ObjectIdField())
    comments=ListField(ObjectIdField())
