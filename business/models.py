from django.db import models
from mongoengine import connect,ObjectIdField,StringField,IntField,ListField,ImageField,DateTimeField, FileField ,BooleanField, Document

connect("EAD_OOAL")
# Create your models here.

class Limited_Offer(Document):
    company_id = StringField(max_length=200)
    created_date = DateTimeField()
    created_user = ObjectIdField()
    offer_count = IntField()
    banner_image = ImageField()
    coupons = ListField(ObjectIdField())

class Limited_Offer_Coupons(Document):
    coupon_code = StringField(max_length=200)
    start_date = DateTimeField()
    expiry_date = DateTimeField()
    discription = StringField(max_length=1000)

class Unlimited_Coupons(Document):
    company_id = StringField(max_length=200)
    coupon_code = StringField(max_length=200)
    created_date = DateTimeField()
    created_user = ObjectIdField()
    banner_image = ImageField()
    discription = StringField(max_length=1000)

class Video_Check(Document):
    video_name = StringField(max_length=100)
    video = FileField()
