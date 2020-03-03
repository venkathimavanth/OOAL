from django.shortcuts import render
from user_auth.decorators import *
from management.models import *
from user_auth.models import *
import datetime
# Create your views here.

@management_required
def addchallenge(request):
    cats = CategoryModel.objects.order_by('category_name')
    type = ChallangeTypeModel.objects.all()
    submissions=TypeOfSubmissionModel.objects.all()
    if request.method == 'GET':
        return render(request,'management/addchallenge.html',{"cats":cats,"type":type,"submissions":submissions})
    elif request.method == 'POST':
        if "name" in request.POST and "category" in request.POST and "type" in request.POST and "hours" in request.POST and "age_restricted" in request.POST and "discription" in request.POST:
            name = request.POST["name"]
            created_date=datetime.datetime.now()
            hours_to_complete = int(request.POST["hours"])
            number_of_reports = 0
            age_restricted=request.POST["age_restricted"]
            discription = request.POST["discription"]
            created_user = None
            category_name = None
            challange_type = None
            type_of_submission=None
            try:
                type_of_submission=TypeOfSubmissionModel.objects.get(type_of_submission=request.POST["submissions"])["id"]
                category_name=CategoryModel.objects.get(category_name=request.POST["category"])["id"]
                challange_type=ChallangeTypeModel.objects.get(challange_type_model=request.POST["type"])["id"]
                created_user= User.objects.get(email=request.session["username"])["id"]
                Challange(name=name,created_date=created_date,hours_to_complete=hours_to_complete,number_of_reports=number_of_reports,age_restricted=age_restricted,discription=discription,type_of_submission=type_of_submission,category_name=category_name,challange_type=challange_type,created_user=created_user).save()
                return redirect("user_auth:managementhome")
            except:
                return render(request,'management/addchallenge.html',{"cats":cats,"type":type,"warning":"Wrong attributes given"})
        else:
            return render(request,'management/addchallenge.html',{"cats":cats,"type":type,"warning":"Fill all attributes"})
    return redirect('user_auth:managementhome')
