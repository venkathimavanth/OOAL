from mongoengine import connect,ObjectIdField,StringField,IntField,ListField,ImageField,Document

connect('EAD_OOAL')


class community(Document):
    name=StringField(max_length=200)
    discription=StringField(max_length=200)
    no_of_participants = IntField(default=0)
    Heads = ListField(ObjectIdField())
    participants = ListField(ObjectIdField())
    group_challanges = ListField(ObjectIdField())
    community_blog = ListField(ObjectIdField())
    photo = ImageField()
