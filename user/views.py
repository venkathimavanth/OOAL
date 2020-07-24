from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from user_auth.decorators import *
from user_auth.models import *
from management.models import *
from user_auth.views import check_user_exists
from user.models import *
from business.models import *
from management.models import FunContent
from django.http import JsonResponse
import base64
import datetime,json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
# import the MongoClient class from the library
from pymongo import MongoClient
mongo_client = MongoClient()
db = mongo_client.EAD_OOAL
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .ead_abusive_sentence_detector import abusive_detect_main
from datetime import date


def get_userprofile(request,id):
    p=Profile.objects.filter(user_id=id)
    prof=None
    got=False
    for prof in p:
        got=True
    return (got,prof)

@login_required
def userhome(request):
    print("called userhome view func in user app")
    ae,user=check_user_exists(request,request.session["username"])
    profile = Profile.objects.get(id = user["profileid"])

    if request.method == "POST":
        if "tought" in request.POST :
            post=Post(
                user_id =  user["id"],
                # user_photo = ImageField()
                created_date=datetime.datetime.now(),

                # isimage = BooleanField(default=False)
                # isvideo = BooleanField(default=False)

                text = request.POST["tought"],
                # image = ImageField()
                # text = StringField(max_length=200)

            )
            post.save()
            addThisPost(request,post,user,profile)
        HttpResponseRedirect("user.views.userhome")

    context={'warning':"Logged in successfully"}
    try:
        daily_challange=DailyChallanges.objects.get(posted_date=datetime.date.today())
        context['daily_challange']=daily_challange
    except:
        pass

    try:
        weekNumber = date.today().isocalendar()[1]
        Weekly_challange=reversed(WeeklyChallanges.objects.filter(posted_week=str(weekNumber)))
        for w in Weekly_challange:
            context['weekly_challange']=w
            break

    except:
        pass

    try:
        ftf=profile["accepted_chall"]
        lis=[]
        for f in ftf:
            lis.append(FriendToFriend.objects.get(id=f))
        context['ftf']=lis
    except:
        pass


    try:
        lo=Limited_Offer.objects.all()
        lis=[]
        for l in lo :
            loc=Limited_Offer_Coupons.objects.get(id=l["coupons"][0])
            if datetime.datetime.now() < loc["expiry_date"]:
                lis.append(l)
        context['Limited_Offer']=lis
    except:
        pass


    feed=profile["myfeed"]
    posts=[]
    for f in feed:
        try:
            p=Post.objects.get(id=f)
            po=dict()
            po["id"]=p["id"]
            po["user_id"]=p["user_id"]
            profile1=Profile.objects.get(user_id=p["user_id"])
            po["username"]=profile1["name"]

            photo= profile1["photo"].grid_id
            col = db.images.chunks.find({"files_id":photo})
            my_string = base64.b64encode(col[0]["data"])
            po["user_photo"]=my_string.decode('utf-8')
            # print(my_string.decode('utf-8'))
            po["created_date"]=p["created_date"]#
            po["isimage"]=p["isimage"]
            po["isvideo"]=p["isvideo"]
            po["text"]=p["text"]

            content = p.content.read()
            base64EncodedStr = base64.b64encode(content)
            content = base64EncodedStr.decode('utf-8')
            po["content"] =content

            po["ischallenge"]=p["ischallenge"]

            if p["ischallenge"]:
                po["challegetype"]=p["challegetype"]
                po["challengeid"]=p["challengeid"]


            po["isad"]=p["isad"]

            if p["isad"]:
                po["adid"]=p["adid"]

            po["likes"]=p["likes"]
            po["comments"]=p["comments"]
            posts.append(po)
        except:
            pass
    context["posts"]=posts[-1:-101:-1]
    context["sfriends"]=returnSuggestedFriends(request)

    # print(context)
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 2)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    return render(request,'registration/loginhome.html',context)



@login_required
def single_post(request):
    if request.method == "GET":
        print("came into single_post")
        post_id = request.GET["postId"]

        username = request.session["username"]
        user = User.objects(email=username)[0]
        profile = Profile.objects.get(user_id=user["id"])

        po=dict()

        p=Post.objects.get(id=post_id)

        po["id"]=p["id"]
        po["user_id"]=p["user_id"]
        profile1=Profile.objects.get(user_id=p["user_id"])
        po["username"]=profile1["name"]

        photo= profile1["photo"].grid_id
        col = db.images.chunks.find({"files_id":photo})
        my_string = base64.b64encode(col[0]["data"])
        po["user_photo"]=my_string.decode('utf-8')
        # print(my_string.decode('utf-8'))
        po["created_date"]=p["created_date"]#
        po["isimage"]=p["isimage"]
        po["isvideo"]=p["isvideo"]
        po["text"]=p["text"]

        content = p.content.read()
        base64EncodedStr = base64.b64encode(content)
        content = base64EncodedStr.decode('utf-8')
        po["content"] =content

        po["ischallenge"]=p["ischallenge"]

        if p["ischallenge"]:
            po["challegetype"]=p["challegetype"]
            po["challengeid"]=p["challengeid"]


        po["isad"]=p["isad"]

        if p["isad"]:
            po["adid"]=p["adid"]

        po['likedBy'] = p['likes']
        po['is_liked_by_curr_user'] = False

        if user['id'] in po['likedBy']:
            po['is_liked_by_curr_user'] = True
        po['likes'] = len(po['likedBy'])


        po["comments"]=p["comments"]
        try:
            pass
        except:
            pass

        my_photo= profile["photo"].grid_id
        my_col = db.images.chunks.find({"files_id":my_photo})
        my_my_string = base64.b64encode(my_col[0]["data"])
        po["ownerphoto"] = my_my_string.decode('utf-8')
        comments = []

        for k in po["comments"]:
            comm = Comment.objects.get(id = k)
            print(comm)
            temp1 = dict()
            temp1['comment'] = comm['message']
            temp1['reports'] = comm['message']
            o = comm['owner']
            own = User.objects(id = o)[0]
            own_p = Profile.objects.get(user_id = o)
            temp1['owner'] = own_p['name']
            photo= own_p["photo"].grid_id
            ph = db.images.chunks.find({"files_id":photo})
            ph_string = base64.b64encode(ph[0]["data"])
            temp1["photo"] = ph_string.decode('utf-8')

            comments.append(temp1)
        count = len(comments)
        print('-------------------------',po["is_liked_by_curr_user"])
        return render(request, 'registration/modal.html', {'myphoto': my_photo,'post': po, 'comments': comments, 'count': count})
    else:
        return HttpResponse("failure")


def createComment(request):
    print("create comment")
    if request.method == "POST":
        ad_user = request.session["username"]
        post_id  =  request.POST["p_id"]
        cmnt = request.POST["msg"]
        a_uid = User.objects(email=ad_user)[0]

        comnt = Comment(message = cmnt, owner= a_uid['id'])
        comnt.save()
        Post.objects(id=post_id).update_one(push__comments=comnt["id"])
        return HttpResponse('Added comment to the post')
    else:
        return HttpResponse('Failure')


def like(request):
    if request.method == 'GET':
        post_id = request.GET['postId']
        username = request.session["username"]
        user = User.objects(email=username)[0]
        profile = Profile.objects.get(user_id=user["id"])
        post = Post.objects.get(id = post_id)

        if user['id'] not in post['likes']:
            post.likedBy.append(user["id"])
            post.save()
        else:
            post.likedBy.remove(user["id"])
            post.save()
        return HttpResponse('Success')
    else:
        return HttpResponse(Failure)


def addThisPost(request,post,user,profile):
    profile["myposts"].append(post["id"])
    profile["myfeed"].append(post["id"])
    profile.save()
    for f in profile["friends"]:
        p=Profile.objects.filter(user_id=f)
        print(p)
        if p:
            for q in p:
                q["myfeed"].append(post["id"])
                q.save()

def dsc(request):
    context=dict()
    ae,user=check_user_exists(request,request.session["username"])
    profile = Profile.objects.get(id = user["profileid"])
    if request.method == "POST":
        if 'file' in request.FILES:
            file = request.FILES['file']
            content_type = 'video/mp4'
            daily_challange=DailyChallanges.objects.get(posted_date=datetime.date.today())
            post=Post(
                user_id =  user["id"],
                user_photo = profile["photo"],
                created_date=datetime.datetime.now(),

                isimage = False,
                isvideo = True,

                text = daily_challange["discription"],
                ischallenge = True,
                challegetype="Daily Single Challange",
                challengeid=daily_challange["id"],
            ).save()
            post.content.put(file,content_type=content_type)
            post.save()
            addThisPost(request,post,user,profile)
            profile["completed"].append(daily_challange["id"])
            profile.save()


    try:
        daily_challange=DailyChallanges.objects.get(posted_date=datetime.date.today())
        context['daily_challange']=daily_challange
        context["completed"] = False
        if daily_challange["id"] in profile["completed"]:
            context["completed"] =True
        # print("-----------------",context["completed"],profile["completed"])
    except:
        pass

    return render(request,'user/dsc.html',context)

def ftf(request,id):
    context=dict()
    ae,user=check_user_exists(request,request.session["username"])
    profile = Profile.objects.get(id = user["profileid"])
    if request.method == "POST":
        if 'file' in request.FILES:
            f=FriendToFriend.objects.get(id=id)
            file = request.FILES['file']
            content_type = 'video/mp4'
            post=Post(
                user_id =  user["id"],
                user_photo = profile["photo"],
                created_date=datetime.datetime.now(),

                isimage = False,
                isvideo = True,

                text = f["discription"],
                ischallenge = True,
                challegetype="Friend to Friend Challange",
                challengeid=f["id"],
            ).save()
            post.content.put(file,content_type=content_type)
            post.save()
            addThisPost(request,post,user,profile)
            profile["accepted_chall"].remove(f["id"])
            profile.save()
            return redirect('user:userhome')

    try:
        f=FriendToFriend.objects.get(id=id)
        if f["id"] in profile["accepted_chall"]:
            context["ftf"]=f
            return render(request,'user/ftf.html',context)
    except:
        pass
    return redirect('user:userhome')


def lo(request,id):
    context=dict()
    ae,user=check_user_exists(request,request.session["username"])
    profile = Profile.objects.get(id = user["profileid"])
    if request.method == "POST":
        if 'file' in request.FILES:
            f=Limited_Offer.objects.get(id=id)
            loc=Limited_Offer_Coupons.objects.get(id=f["coupons"][0])

            file = request.FILES['file']
            content_type = 'video/mp4'
            post=Post(
                user_id =  user["id"],
                user_photo = profile["photo"],
                created_date=datetime.datetime.now(),

                isimage = False,
                isvideo = True,

                text = loc["discription"],
                ischallenge = True,
                challegetype="Limited Offer",
                challengeid=f["id"],
            ).save()
            post.content.put(file,content_type=content_type)
            post.save()
            addThisPost(request,post,user,profile)

            cupon=Cupon(
                offerid = f["id"],
                couponid = loc["id"]
            )
            cupon.save()
            profile["cupons"].append(cupon["id"])
            profile.save()
            return redirect('user:userhome')

    try:
        context=dict()
        f=Limited_Offer.objects.get(id=id)
        loc=Limited_Offer_Coupons.objects.get(id=f["coupons"][0])
        if datetime.datetime.now() < loc["expiry_date"]:
            context['offer']=f
            context['cupon']=loc
        completed=False
        for c in profile["cupons"]:
            cou=Cupon.objects.get(id=c)
            if f.id == cou.offerid:
                completed=True
        context["completed"]=completed
        return render(request,'user/lo.html',context)
    except:
        pass
    return redirect('user:userhome')


@login_required
def friends(request):
    print("called friends view func")
    ae,user=check_user_exists(request,request.session["username"])
    profile = Profile.objects.get(id = user["profileid"])
    content=list()
    for f in profile["friends"]:
        temp=dict()
        reqby = User.objects.get(id=f)
        reqbyprof = Profile.objects.get(user_id=f)
        temp["name"] = reqbyprof["name"]
        temp["discription"] = reqbyprof["discription"]
        try:
            temp["discription"] = temp["discription"][:40] + "....."
        except:
            pass
        temp["email"] = reqby["email"]
        photo= reqbyprof["photo"].grid_id
        col = db.images.chunks.find({"files_id":photo})
        my_string = base64.b64encode(col[0]["data"])
        temp["photo"] = my_string.decode('utf-8')
        content.append(temp)
    # print(content)
    return render(request,"user/friends.html",{"content":content})



@login_required
def pendingrequests(request):
    print("called findfriends view func")
    ae,user=check_user_exists(request,request.session["username"])
    profile = Profile.objects.get(id = user["profileid"])
    content=list()
    for f in profile["pending_friend_requests"]:
        temp=dict()
        reqby = User.objects.get(id=f)
        reqbyprof = Profile.objects.get(user_id=f)
        temp["name"] = reqbyprof["name"]
        temp["discription"] = reqbyprof["discription"]
        try:
            temp["discription"] = temp["discription"][:40] + "....."
        except:
            pass
        temp["email"] = reqby["email"]
        photo= reqbyprof["photo"].grid_id
        col = db.images.chunks.find({"files_id":photo})
        my_string = base64.b64encode(col[0]["data"])
        temp["photo"] = my_string.decode('utf-8')
        content.append(temp)
    # print(content)
    return render(request,"user/pendingrequests.html",{"content":content})



@login_required
def findfriends(request):
    print("called findfriends view func")
    ae,user=check_user_exists(request,request.session["username"])
    profile = Profile.objects.get(id = user["profileid"])
    content=list()
    for h in User.objects.all()[:16]:
        if h["id"] == user["id"] or h["id"] in profile["friends"]:
            continue
        f = h["id"]
        temp=dict()
        reqby = User.objects.get(id=f)
        reqbyprof = Profile.objects.get(user_id=f)
        temp["name"] = reqbyprof["name"]
        temp["discription"] = reqbyprof["discription"]
        try:
            temp["discription"] = temp["discription"][:40] + "....."
        except:
            pass
        temp["email"] = reqby["email"]
        photo= reqbyprof["photo"].grid_id
        col = db.images.chunks.find({"files_id":photo})
        my_string = base64.b64encode(col[0]["data"])
        temp["photo"] = my_string.decode('utf-8')
        content.append(temp)

    return render(request,"user/findfriends.html",{"content":content})


def returnSuggestedFriends(request):
    ae,user=check_user_exists(request,request.session["username"])
    profile = Profile.objects.get(id = user["profileid"])
    content=list()
    for h in User.objects.all()[:8]:
        if h["id"] == user["id"] or h["id"] in profile["friends"]:
            continue
        f = h["id"]
        temp=dict()
        reqby = User.objects.get(id=f)
        reqbyprof = Profile.objects.get(user_id=f)
        temp["name"] = reqbyprof["name"]
        temp["discription"] = reqbyprof["discription"]
        try:
            temp["discription"] = temp["discription"][:40] + "....."
        except:
            pass
        temp["email"] = reqby["email"]
        photo= reqbyprof["photo"].grid_id
        col = db.images.chunks.find({"files_id":photo})
        my_string = base64.b64encode(col[0]["data"])
        temp["photo"] = my_string.decode('utf-8')
        content.append(temp)
    return content

@login_required
def viewprofile(request,email):
    print("called viewprofile view func")
    e,u = check_user_exists(request,email)
    ae,user=check_user_exists(request,request.session["username"])
    message=""
    if request.method == "POST":
        x=abusive_detect_main(request.POST["discription"])
        if int(x) in [3,4]:
            message = "Your Challange Is Harmfull"
        else:
            f = FriendToFriend(
                user_id =  user["id"],
                created_date=datetime.datetime.now(),
                name = request.POST["name"],
                discription = request.POST["discription"],
            ).save()
            profile1=Profile.objects.get(id=u["profileid"])
            profile1['accepted_chall'].append(f["id"])
            profile1.save()
    if e and ae and u["profile_created"] and user["profile_created"] and ( u["id"] != user["id"] ):
        profile1=Profile.objects.get(id=u["profileid"])
        profile2=Profile.objects.get(id=user["profileid"])
        friends=0
        # print(profile1["pending_friend_requests"])
        for f in profile1["friends"]:
            if profile2["user_id"] ==  f :
                friends=2
        for f in profile1["pending_friend_requests"]:
            if profile2["user_id"] ==  f :
                friends=1
        for f in profile2["pending_friend_requests"]:
            if profile1["user_id"] ==  f :
                friends=3
        # photo= profile1["photo"].toString('base64');
        photo= profile1["photo"].grid_id
        col = db.images.chunks.find({"files_id":photo})
        my_string = base64.b64encode(col[0]["data"])
        # for c in col:
        context={
            "name" : profile1["name"],
            "discription" : profile1["discription"],
            "email" : u["email"],
            "photo" : my_string.decode('utf-8'),
            "friends" : friends,
            "message":message
        }
        return render(request,"user/viewprofile.html",context)
    return redirect("user:friends")


def autocompleteModel(request):
    print("ASDFGFDSASDF")
    if request.method == "POST":
        search_text= request.POST['search_text']
    else:
        search_text=""
    profile = Profile.objects.filter(name__startswith=search_text)[:16]
    content=list()
    for p in profile:
        temp=dict()
        temp["name"] = p["name"]
        temp["discription"] = p["discription"]
        us = User.objects.get(id=p["user_id"])
        temp["email"] = us["email"]

        photo= p["photo"].grid_id
        col = db.images.chunks.find({"files_id":photo})
        my_string = base64.b64encode(col[0]["data"])
        my_string=my_string.decode('utf-8')
        temp["photo"] = my_string


        content.append(temp)
    # print(content)
    return render_to_response('user/li.html',{"content":content})

@login_required
def viewmyprofile(request):
    ae,user=check_user_exists(request,request.session["username"])
    if ae:
        pe,profile=get_userprofile(request,user["id"])
        if pe:
            temp={"profile":profile,"email":user["email"]}
            photo= profile["photo"].grid_id
            col = db.images.chunks.find({"files_id":photo})
            my_string = base64.b64encode(col[0]["data"])
            my_string=my_string.decode('utf-8')
            temp["photo"] = my_string
            temp["posts_count"] = len(profile["myposts"])
            temp["friends"] = len(profile["friends"])
            temp["sfriends"]=returnSuggestedFriends(request)
            cu=[]
            y=0
            try:
                x=[]
                for c in profile["cupons"][::-1]:
                    print("--")
                    t=dict()
                    cupon=Cupon.objects.get(id=c)
                    t["offer"]=Limited_Offer.objects.get(id=cupon.offerid)
                    t["cupon"]=Limited_Offer_Coupons.objects.get(id=cupon.couponid)
                    x.append(t)
                    if y%2 == 1:
                        cu.append(x)
                        x=[]
                    y=y+1
                if x:
                    cu.append(x)
            except:
                pass
            temp["cupons"]=cu
            return render(request,"user/viewmyprofile.html",temp)
    return redirect("user_auth:loggedinhome")


@login_required
def challanges(request):
    ae,user=check_user_exists(request,request.session["username"])
    if ae:
        pe,profile=get_userprofile(request,user["id"])
        if pe:
            dc=None
            try:
                dc=DailyChallanges.objects.get(posted_date=datetime.date.today())
            except:
                pass
            return render(request,"user/challanges.html",{"profile":profile,"email":user["email"],"dc":dc})
    return redirect("user_auth:loggedinhome")




def viewfullprofile(request,email):
    return redirect("user:viewprofile",email)


def add_deop_req(request,email,type):
    if type == "1":
        return redirect("user:friend_req_handle",email,"5")
    elif type=="0":
        return redirect("user:friend_req_handle",email,"4")


def friend_req_handle(request,email,test):
    print("called friend_req_handle view func")
    e,u = check_user_exists(request,email)
    ae,user=check_user_exists(request,request.session["username"])
    if e and ae and u["profile_created"] and user["profile_created"] and ( u["id"] != user["id"] ):
        profile1=Profile.objects.get(id=u["profileid"])
        profile2=Profile.objects.get(id=user["profileid"])
        friends="0"
        for f in profile1["friends"]:
            if profile2["user_id"] ==  f :
                friends="2"
        for f in profile1["pending_friend_requests"]:
            if profile2["user_id"] ==  f :
                friends="1"
        for f in profile2["pending_friend_requests"]:
            if profile1["user_id"] ==  f :
                friends="3"
        if test == "0" and friends == "0":
            if user["id"] not in profile1["pending_friend_requests"]:
                profile1["pending_friend_requests"] += [ user["id"], ]
                profile1.save()
        elif test == "1" and friends == "1":
            try:
                profile1["pending_friend_requests"].remove(user["id"])
                profile1.save()
            except:
                pass
        elif test =="2" and friends == "2":
            try:
                profile1["friends"].remove(user["id"])
                profile1.save()
                profile2["friends"].remove(u["id"])
                profile2.save()
            except:
                pass
        elif test =="3" and friends == "3":
            try:
                profile2["pending_friend_requests"].remove(u["id"])
                profile2["friends"].append(u["id"])
                profile2.save()
                profile1["friends"].append(user["id"])
                profile1.save()
            except:
                pass
        elif test =="5" and friends == "3":
            try:
                profile2["pending_friend_requests"].remove(u["id"])
                profile2["friends"].append(u["id"])
                profile2.save()
                profile1["friends"].append(user["id"])
                profile1.save()
                return redirect('user:pendingrequests')
            except:
                pass
        elif test =="4" and friends == "3":
            try:
                profile2["pending_friend_requests"].remove(u["id"])
                profile2.save()
                return redirect('user:pendingrequests')
            except:
                pass

        return redirect('user:viewprofile',email)
    return redirect("user_auth:loggedinhome")

@login_required
def fun_view(request):
    all_content = []

    for fun_instance in FunContent.objects:
        content = fun_instance.content.read()
        base64EncodedStr = base64.b64encode(content)
        content = base64EncodedStr.decode('utf-8')
        user_id=fun_instance.created_user
        profile = Profile.objects.filter(user_id=user_id).first()
        user = profile.name
        pic=profile.photo.read()
        picbase64EncodedStr = base64.b64encode(pic)
        pic = picbase64EncodedStr.decode('utf-8')

        print("\n",user)
        all_content.append({'content': content,
                            'user':user,
                            'pic': pic,
                            'content_type': fun_instance.content.content_type,
                            'description':fun_instance.description,
                            'is_image': fun_instance.content.is_image})

    # return render(request, template, {"all_content": all_content})
    print("\nReady to render\n")
    page = request.GET.get('page', 1)
    paginator = Paginator(all_content, 2)
    try:
        all_content = paginator.page(page)
    except PageNotAnInteger:
        all_content = paginator.page(1)
    except EmptyPage:
        all_content = paginator.page(paginator.num_pages)
    # return render(request, 'business/test.html', {'all_content': all_content})
    return render(request, 'user/fun_view.html', {'all_content': all_content})
