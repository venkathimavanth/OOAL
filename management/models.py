from mongoengine import connect,ObjectIdField,StringField,IntField,ListField,FileField,ImageField,DateTimeField, BooleanField, Document

connect("EAD_OOAL")

class CategoryModel(Document):
    category_name = StringField(max_length=200)

class ChallangeTypeModel(Document):
    challange_type_model = StringField(max_length=200)


class TypeOfSubmissionModel(Document):
    type_of_submission = StringField(max_length=200)


class Challange(Document):
    name = StringField(max_length=200)
    created_date=DateTimeField()
    created_user= ObjectIdField()
    category_name = ObjectIdField()
    challange_type=ObjectIdField()
    type_of_submission=ObjectIdField()
    hours_to_complete = IntField(default=0)
    number_of_reports = IntField(default=0)
    age_restricted=BooleanField(default=False)
    discription = StringField(max_length=1000)


class DailyChallanges(Document):
    name = StringField(max_length=200)
    created_date=DateTimeField()
    posted_date=DateTimeField(unique=True)
    number_of_reports = IntField(default=0)
    age_restricted=BooleanField(default=False)
    discription = StringField(max_length=1000)

class FunContent(Document):
    created_date = DateTimeField()
    created_user= ObjectIdField()
    content = FileField()
    description = StringField(max_length=1000)

class Report(Document):
    user_id = ObjectIdField()
    time = DateTimeField()
    post_id = ObjectIdField()
    problem = StringField(max_length=1000)
