from django.shortcuts import render,render_to_response
from user_auth.decorators import *
from management.models import *
from user_auth.models import *
import datetime,base64
from django.contrib import messages
from user.models import Post
from datetime import date
# Create your views here.

@management_required
def addweeklychallenge(request):
    print("called addchallenge view func")
    cats = CategoryModel.objects.order_by('category_name')
    type = ChallangeTypeModel.objects.all()
    submissions=TypeOfSubmissionModel.objects.all()
    # print(submissions)
    if request.method == 'GET':
        return render(request,'management/addchallenge.html',{"cats":cats,"type":type,"submissions":submissions})
    elif request.method == 'POST':
        print("-----------------------------------")
        if "name" in request.POST  and "discription" in request.POST:
            name = request.POST["name"]
            p_date=datetime.datetime.now()
            print("-----------------------------------")
            d=WeeklyChallanges(name=name,created_date=datetime.datetime.now(),posted_year=str(p_date.year),posted_week=str(date.today().isocalendar()[1]),discription=request.POST["discription"])
            d.save()
            return redirect('user_auth:managementhome')
            try:
                print("saved")
            except:
                pass
            try:
                created_date=datetime.datetime.now()
                hours_to_complete = int(request.POST["hours"])
                number_of_reports = 0
                age_restricted=request.POST["age_restricted"]
                discription = request.POST["discription"]
                created_user = None
                category_name = None
                challange_type = None
                type_of_submission=None
                type_of_submission=TypeOfSubmissionModel.objects.get(type_of_submission=request.POST["submissions"])["id"]
                category_name=CategoryModel.objects.get(category_name=request.POST["category"])["id"]
                challange_type=ChallangeTypeModel.objects.get(challange_type_model=request.POST["type"])["id"]
                created_user= User.objects.get(email=request.session["username"])["id"]
                Challange(name=name,created_date=created_date,hours_to_complete=hours_to_complete,number_of_reports=number_of_reports,age_restricted=age_restricted,discription=discription,type_of_submission=type_of_submission,category_name=category_name,challange_type=challange_type,created_user=created_user).save()
                return redirect("user_auth:managementhome")
            except:
                return render(request,'management/weeklychallange.html',{"cats":cats,"type":type,"submissions":submissions,"warning":"Wrong attributes given"})
        else:
            return render(request,'management/weeklychallange.html',{"cats":cats,"type":type,"submissions":submissions,"warning":"Fill all attributes"})
    return redirect('user_auth:managementhome')

@management_required
def addchallenge(request):
    print("called addchallenge view func")
    cats = CategoryModel.objects.order_by('category_name')
    type = ChallangeTypeModel.objects.all()
    submissions=TypeOfSubmissionModel.objects.all()
    # print(submissions)
    if request.method == 'GET':
        return render(request,'management/addchallenge.html',{"cats":cats,"type":type,"submissions":submissions})
    elif request.method == 'POST':
        if "name" in request.POST and "date" in request.POST and "discription" in request.POST:
            name = request.POST["name"]
            p_date=datetime.datetime.strptime(request.POST["date"], '%Y-%m-%d').date()
            print("-----------------------------------")
            d=DailyChallanges(name=name,created_date=datetime.datetime.now(),posted_date=p_date,discription=request.POST["discription"])
            d.save()
            try:
                print("saved")
            except:
                pass
            try:
                created_date=datetime.datetime.now()
                hours_to_complete = int(request.POST["hours"])
                number_of_reports = 0
                age_restricted=request.POST["age_restricted"]
                discription = request.POST["discription"]
                created_user = None
                category_name = None
                challange_type = None
                type_of_submission=None
                type_of_submission=TypeOfSubmissionModel.objects.get(type_of_submission=request.POST["submissions"])["id"]
                category_name=CategoryModel.objects.get(category_name=request.POST["category"])["id"]
                challange_type=ChallangeTypeModel.objects.get(challange_type_model=request.POST["type"])["id"]
                created_user= User.objects.get(email=request.session["username"])["id"]
                Challange(name=name,created_date=created_date,hours_to_complete=hours_to_complete,number_of_reports=number_of_reports,age_restricted=age_restricted,discription=discription,type_of_submission=type_of_submission,category_name=category_name,challange_type=challange_type,created_user=created_user).save()
                return redirect("user_auth:managementhome")
            except:
                return render(request,'management/addchallenge.html',{"cats":cats,"type":type,"submissions":submissions,"warning":"Wrong attributes given"})
        else:
            return render(request,'management/addchallenge.html',{"cats":cats,"type":type,"submissions":submissions,"warning":"Fill all attributes"})
    return redirect('user_auth:managementhome')




@management_required
def dailychallanges(request):
    print("called management:dailychallanges view func")
    obj=None
    prev=False
    next=False
    date=datetime.datetime.now()
    if DailyChallanges.objects.filter(posted_date=datetime.date.today() - datetime.timedelta(days=1)):
        prev= True
    if DailyChallanges.objects.filter(posted_date=datetime.date.today() + datetime.timedelta(days=1)):
        next= True
    try:
        obj=DailyChallanges.objects.get(posted_date=datetime.date.today())
        date=obj["posted_date"]
    except:
        pass
    return render(request,'management/dailychallanges.html',{"obj":obj,"next":next,"prev":prev,"date":date})


def findprev(request):
    if request.method == 'POST':
        search_text= request.POST['search_text']
        search_text= search_text[:-10]
        obj=DailyChallanges.objects.get(posted_date=datetime.datetime.strptime(search_text, '%B %d, %Y')- datetime.timedelta(days=1))
        prev=False
        if DailyChallanges.objects.filter(posted_date=datetime.datetime.strptime(search_text, '%B %d, %Y')- datetime.timedelta(days=2)):
            prev= True
        return render_to_response('management/find.html',{"obj":obj,"next":True,"prev":prev,"date":datetime.datetime.strptime(search_text, '%B %d, %Y')- datetime.timedelta(days=1)})


def findnext(request):
    if request.method == 'POST':
        search_text= request.POST['search_text']
        search_text= search_text[:-10]
        obj=DailyChallanges.objects.get(posted_date=datetime.datetime.strptime(search_text, '%B %d, %Y')+ datetime.timedelta(days=1))
        next=False
        if DailyChallanges.objects.filter(posted_date=datetime.datetime.strptime(search_text, '%B %d, %Y')+ datetime.timedelta(days=2)):
            next= True
        return render_to_response('management/find.html',{"obj":obj,"next":next,"prev":True,"date":datetime.datetime.strptime(search_text, '%B %d, %Y')+ datetime.timedelta(days=1)})



@management_required
def managementhome(request):
    print("called management:managementhome view func")
    return render(request,'management/managementhome.html',{'warning':"Logged in successfully"})

@management_required
def fun_upload(request):
    template = 'management/fun_upload.html'
    if request.method == 'POST':
        print('\nPOST')
        if 'file' in request.FILES and 'content' in request.POST and 'description' in request.POST:
            print('Correct request')
            description = request.POST['description']
            content = request.POST['content']
            file = request.FILES['file']
            if content == 'image':
                content_type = 'image/jpeg'
                is_image = True
            else:
                content_type = 'video/mp4'
                is_image = False
            created_date = datetime.datetime.now()
            created_user = User.objects.get(email=request.session["username"])["id"]
            instance = FunContent(description = description,created_date=created_date,created_user=created_user).save()
            instance.content.put(file,content_type=content_type,is_image=is_image)
            instance.save()
            messages.success(request, 'Post sucessfully uploaded')
            return render(request,template)
        else:
            messages.error(request, 'Please fill all the feilds')
            return render(request, template)
    else:
        return render(request,template)

@management_required
def report_portal(request):
    template = 'management/report_portal.html'
    return render(request,template)


def addcatogries(request):
    if request.method == "POST":
        category_name=request.POST["category"]
        name = request.POST["name"]
        print(category_name)
        if category_name == "CategoryModel":
                c=CategoryModel(category_name=name)
                c.save()
        elif category_name == "ChallangeTypeModel":
                c=ChallangeTypeModel(challange_type_model=name)
                c.save()
        elif category_name == "TypeOfSubmissionModel":
                c=TypeOfSubmissionModel(type_of_submission=name)
                c.save()
    return render(request,'management/addcatogries.html',{})


def report(request):
    if request.method == 'POST':
        if 'problem' in request.POST:
            pass
        else:
            messages.error('Please fill all feilds')
            return
    else:
        template='management/get_report.html'
        post_id = request.GET.get('post')
        post = Post.objects.filter(id = post_id).first()
        post_img = post.user_photo.read()
        imgbase64EncodedStr = base64.b64encode(post_img)
        post_img = imgbase64EncodedStr.decode('utf-8')
        context = {'post_img':post_img}
        return render(request,template,context)
    # pass
# def temp(request):
#     print("oyyeoyye")
#     obj=DailyChallanges(
#         name = "say hello",
#         posted_date=datetime.date.today(),
#         created_date=datetime.datetime.now(),
#         discription = "do it faster",
#         ).save()
#     return render(request,'management/dailychallanges.html',{})
