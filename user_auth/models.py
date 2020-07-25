from mongoengine import connect,ObjectIdField,StringField,IntField,ListField,ImageField,DateTimeField, BooleanField, Document,FileField

connect("EAD_OOAL")


class User(Document):
    email = StringField(max_length=200,unique = True)
    password = StringField(max_length=1000)
    created_date=DateTimeField()
    email_verified=BooleanField(default=False)
    profile_created=BooleanField(default=False)
    user_type = StringField(max_length=10)
    profileid=  ObjectIdField()



class Cupon(Document):
    offerid = ObjectIdField()
    couponid = ObjectIdField()


class Profile(Document):
    name=StringField(max_length=200)
    discription=StringField(max_length=200)
    user_id =  ObjectIdField(unique = True)
    # photo = ImageField()
    photo=FileField()
    age = IntField(default=0)
    city = StringField(max_length=200)
    country = StringField(max_length=200)
    parental_account = BooleanField(default=False)
    parental_password = StringField(max_length=1000)
    total_no_challenges = IntField(default=0)
    total_no_rewards = IntField(default=0)
    xp = IntField(default=0)
    number_of_followers = IntField(default=0)
    friends = ListField(ObjectIdField())
    pending_friend_requests = ListField(ObjectIdField())
    accepted_chall=ListField(ObjectIdField())
    completed=ListField(ObjectIdField())
    cupons=ListField(ObjectIdField())
    clans_registered = ListField(ObjectIdField())
    messages = ListField(ObjectIdField())
    myposts=ListField(ObjectIdField())
    myfeed=ListField(ObjectIdField())
