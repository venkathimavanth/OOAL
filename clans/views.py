import clans
from user_auth.models import User,Profile
import datetime,bcrypt,hashlib
from django.shortcuts import render,redirect, render_to_response, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from user_auth.decorators import login_required,management_required
from user_auth.views import check_user_exists
from django.core.mail import EmailMessage, send_mail
from rest_framework.views import APIView
from .models import community, Comment, clanChallange,challange
from .models import GroupPost as Post
from chat.models import Message, GroupMessage
from management.models import Challange
import datetime


import base64
import datetime,json

# Create your views here.

# import the MongoClient class from the library
from pymongo import MongoClient
mongo_client = MongoClient()
db = mongo_client.EAD_OOAL



@login_required
def like_post(request,post_id):
    username = request.session["username"]
    user = User.objects(email=username)[0]
    profile = Profile.objects.get(user_id=user["id"])
    post = Post.objects.get(id=post_id)
    post.likes += 1
    post.likedBy.append(user["id"])
    post.save()
    clan = community.objects.all()
    print(len(clan))
    for c in clan:
        print(c.community_blog)
        print(post.id)
        if post.id in c.community_blog:
            return redirect('community:clan-show',clan_id = c.id)



@login_required
def unlike_post(request,post_id):
    username = request.session["username"]
    user = User.objects(email=username)[0]
    profile = Profile.objects.get(user_id=user["id"])
    post = Post.objects.get(id=post_id)
    post.likes -= 1
    post.likedBy.remove(user["id"])
    post.save()
    clan = community.objects.all()
    print(len(clan))
    for c in clan:
        print(c.community_blog)
        print(post.id)
        if post.id in c.community_blog:
            return redirect('community:clan-show',clan_id = c.id)



@login_required
def add_challange(request,clan_id):
    print("got into add chalng")
    if request.method == 'POST':
        print("got into add_chlng POST")
        if "name" in request.POST and "discription" in request.POST :
            username = request.session["username"]
            uid = User.objects(email=username)[0]
            print("uid",uid["id"])
            name = request.POST["name"]
            complete_date = request.POST["date"]
            discription = request.POST["discription"]

            challange = clanChallange(name=name,created_date=datetime.datetime.now(),discription=discription,complete_date=complete_date)
            challange.owner = uid["id"]
            challange.community_id = clan_id
            challange.save()
            community.objects(id=clan_id).update_one(push__group_challanges=challange.id)
            return redirect('community:clan-show',clan_id = clan_id)
        else:
            return render(request,'clans/clan_show.html',{"warning":"Please fill all the blanks correctly"})
    return redirect('user_auth:home')

@login_required
def submit_challanges(request,challange_id):
    print("submit_challanges")
    if request.method == 'POST':
        print("got into submit_challanges")
        if "photo" in request.FILES :
            username = request.session["username"]
            uid = User.objects(email=username)[0]
            photo=request.FILES["photo"]
            description = request.POST["discription"]

            ch = challange(done_by = uid['id'],discription=description)
            ch.proof_of_completion.put(photo, content_type = 'image/jpeg')
            ch.sent_for_review = True
            ch.clanChallange_id = challange_id
            ch.save()
            print(ch.id)
            clan = clanChallange.objects.get(id = challange_id)
            clanChallange.objects(id=challange_id).update_one(push__challange=ch.id)
            clan_id = clan['community_id']

            return redirect('community:show_challanges',clan_id = clan_id)

    #     else:
    #         return render(request,'clans/clans.html',{"warning":"Please fill all the blanks"})
    # print('hiii')
    #return redirect('community:clan-show',clan_id = clan_id)



@login_required
def post(request,clan_id):
    print("uploading a post")
    if request.method == 'POST':
        print("got into clan_post POST")
        if "photo" in request.FILES :
            username = request.session["username"]
            uid = User.objects(email=username)[0]
            print("uid",uid["id"])
            photo=request.FILES["photo"]
            description = request.POST["discription"]

            post=Post(description=description)
            post.image.put(photo, content_type = 'image/jpeg')
            post.owner = uid["id"]
            post.save()
            community.objects(id=clan_id).update_one(push__community_blog=post["id"])

            return redirect('community:clan-show',clan_id = clan_id)
        else:
            return render(request,'clans/clans.html',{"warning":"Please fill all the blanks"})
    print('hiii')
    return redirect('community:clan-show',clan_id = clan_id)



@login_required
def create_clan(request):
    print("got into create_clan")
    if request.method == 'POST':
        print("got into create_clan POST")
        if "photo" in request.FILES and "name" in request.POST and "discription" in request.POST:
            username = request.session["username"]
            uid = User.objects(email=username)[0]
            print("uid",uid["id"])
            name = request.POST["name"]
            photo=request.FILES["photo"]
            discription = request.POST["discription"]

            clan=community(name=name,discription=discription)
            clan.photo.put(photo, content_type = 'image/jpeg')
            clan.Heads.append(uid["id"])
            clan.no_of_participants += 1
            clan.participants.append(uid["id"])
            clan.save()
            print(clan["id"])
            Profile.objects(user_id=uid["id"]).update_one(push__clans_registered=clan["id"])

            return redirect('community:clan-home')
        else:
            return render(request,'clans/clans.html',{"warning":"Please fill all the blanks"})
    return redirect('user_auth:home')


@login_required
def review_challanges(request,clan_id):
    username = request.session["username"]
    user = User.objects.get(email=username)
    clan = community.objects.get(id=clan_id)
    clan_challenges_toberew = []

    print(clan['group_challanges'])
    for ch in clan['group_challanges']:
        c = clanChallange.objects.get(id = ch)

        for challang in c['challange']:
            chall = challange.objects.get(id = challang)
            if not chall['accepted_by_head'] and chall['sent_for_review']:
                temp = dict()
                temp['discription'] = c['discription']
                profile = Profile.objects.get(user_id = chall['done_by'])
                temp['person_name'] = profile['name']
                photo= profile["photo"].grid_id
                col = db.images.chunks.find({"files_id":photo})
                my_string = base64.b64encode(col[0]["data"])
                my_string=my_string.decode('utf-8')
                temp["person_photo"] = my_string
                temp['id'] = challang
                proof = chall['proof_of_completion'].grid_id
                col = db.images.chunks.find({"files_id":proof})
                my_string1 = base64.b64encode(col[0]["data"])
                my_string1=my_string1.decode('utf-8')
                temp['proof'] = my_string1
                temp['remarks'] = chall['discription']
                clan_challenges_toberew.append(temp)

    return render(request, 'clans/review_challanges.html',{"clan_challenges_toberew":clan_challenges_toberew})


@login_required
def accept_challange(request,chall_id):
    chall = challange.objects.get(id = chall_id)
    chall['accepted_by_head'] = True
    clanchall_id = chall['clanChallange_id']
    clanchall = clanChallange.objects.get(id = clanchall_id)
    clan_id = clanchall['community_id']
    chall.save()

    return redirect('community:review_challanges',clan_id = clan_id)

@login_required
def reject_challange(request,chall_id):
    chall = challange.objects.get(id = chall_id)
    chall['sent_for_review'] = False
    clanchall_id = chall['clanChallange_id']
    clanchall = clanChallange.objects.get(id = clanchall_id)
    clan_id = clanchall['community_id']
    chall.save()
    return redirect('community:review_challanges',clan_id = clan_id)



@login_required
def show_challanges(request,clan_id):
    username = request.session["username"]
    user = User.objects.get(email=username)
    clan = community.objects.get(id=clan_id)
    clan_challenges_today = []
    clan_challenges = []
    status = 'Not Completed'
    print(clan['group_challanges'])
    for ch in clan['group_challanges']:
        c = clanChallange.objects.get(id = ch)
        strt = c['created_date'].strftime('%Y-%m-%d')
        comp = c['complete_date'].strftime('%Y-%m-%d')
        tod = datetime.date.today().strftime('%Y-%m-%d')
        for l in c['challange']:
            k = challange.objects.get(id = l)
            if k['done_by'] == user['id']:
                if k['sent_for_review'] and not k['accepted_by_head']:
                    status = 'being reviewed'
                if k['sent_for_review'] and k['accepted_by_head']:
                    status = 'Completed'


        if int(tod[:4]) <= int(comp[:4]):
            if int(tod[5:7]) <= int(comp[5:7]):
                if int(tod[8:10]) <= int(comp[8:10]):
                    print(c['created_date'].strftime('%Y-%m-%d'))
                    print(datetime.date.today().strftime('%Y-%m-%d'))
                    tempc = dict()
                    tempc['id'] = ch
                    tempc['name'] = c['name']
                    tempc['discription'] = c['discription']
                    tempc['deadline'] = c['complete_date']
                    tempc['status'] = status
                    is_owner = False
                    if c['owner'] == user['id']:
                        is_owner = True
                    tempc['is_owner'] = is_owner

                    if strt == tod and comp == tod:
                        clan_challenges_today.append(tempc)

                    else:
                        clan_challenges.append(tempc)

    return render(request, 'clans/show_challanges.html',{"clan_challenges":clan_challenges,'clan_challenges_today':clan_challenges_today})





@login_required
def clanHome(request):
    print('I am in clan home')
    username = request.session["username"]
    user = User.objects.get(email=username)
    profile = Profile.objects.get(user_id=user["id"])



    clans1 = []
    for i in profile["clans_registered"]:
        clan1 = community.objects.get(id=i)
        temp = dict()
        temp['name'] = clan1['name']
        temp['clan_id'] = clan1['id']
        temp['description'] = clan1['discription']
        photo= clan1["photo"].grid_id
        col = db.images.chunks.find({"files_id":photo})
        my_string = base64.b64encode(col[0]["data"])
        temp['clan_photo'] = my_string.decode('utf-8')
        list = []
        for j in clan1['participants']:
            p =  Profile.objects.get(user_id=j)
            photo1= p["photo"].grid_id
            col1 = db.images.chunks.find({"files_id":photo1})
            my_string1 = base64.b64encode(col1[0]["data"])
            list.append(my_string1.decode('utf-8'))

        temp['members_photos'] = list

        clans1.append(temp)
    #print(clans)
    
    return render(request,'clans/clans.html',{"clans1": clans1})

@login_required
def clan_show(request, clan_id):
    username = request.session["username"]
    user = User.objects(email=username)[0]
    profile = Profile.objects(user_id=user["id"])[0]
    clan = community.objects(id=clan_id)[0]
    clan_users = []
    
    print(clan)
    return render(request, 'clans/clan_show.html', {"clan_id":clan_id})

@login_required
def add_clan_user(request, clan_id):
    ae,user=check_user_exists(request,request.session["username"])
    profile = Profile.objects.get(id = user["profileid"])
    content=list()
    for h in User.objects.all()[:16]:
        if h["id"] == user["id"]:
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
    return render(request, 'clans/clan_add_user.html',{"content":content, "clan_id":clan_id})






@login_required
def clan_show(request, clan_id):
    username = request.session["username"]
    user = User.objects(email=username)[0]
    profile = Profile.objects.get(user_id=user["id"])
    clan = community.objects.get(id=clan_id)
    clan_id = clan['id']
    is_head = False
    if user['id'] in clan['Heads']:

        is_head = True


    clan_challenges_today = []
    clan_challenges = []
    print(clan['group_challanges'])
    for ch in clan['group_challanges']:
        c = clanChallange.objects.get(id = ch)
        strt = c['created_date'].strftime('%Y-%m-%d')
        comp = c['complete_date'].strftime('%Y-%m-%d')
        tod = datetime.date.today().strftime('%Y-%m-%d')
        if int(tod[:4]) <= int(comp[:4]):
            if int(tod[5:7]) <= int(comp[5:7]):
                if int(tod[8:10]) <= int(comp[8:10]):
                    print(c['created_date'].strftime('%Y-%m-%d'))
                    print(datetime.date.today().strftime('%Y-%m-%d'))
                    tempc = dict()
                    tempc['name'] = c['name']
                    tempc['discription'] = c['discription']
                    if strt == tod and comp == tod:
                        clan_challenges_today.append(tempc)

    print(clan_challenges_today)


    clan_members = []

    for j in clan['participants']:
        temp1 = dict()
        p =  Profile.objects.get(user_id=j)
        photo1= p["photo"].grid_id
        col1 = db.images.chunks.find({"files_id":photo1})
        my_string1 = base64.b64encode(col1[0]["data"])
        temp1['photo'] = my_string1.decode('utf-8')
        print(p['name'])
        temp1['name'] = p['name']
        temp1['discription'] = p['discription']
        temp1['is_friends'] = False
        u = User.objects.get(id = p['user_id'])
        temp1['email'] = u['email']
        if user['id'] in p['friends'] :
            temp1['is_friends'] = True

        clan_members.append(temp1)

    clan_posts = []
    photo= profile["photo"].grid_id
    col1 = db.images.chunks.find({"files_id":photo})
    my_string1 = base64.b64encode(col1[0]["data"])

    for c in clan['community_blog']:
        temp = dict()
        post = Post.objects.get(id = c)
        temp['id'] = post['id']
        temp['owner'] = profile['name']

        temp['createdAt'] = post['createdAt']
        temp['likes'] = post['likes']
        temp['likedBy'] = post['likedBy']
        temp['is_liked_by_curr_user'] = False

        if user['id'] in post['likedBy']:
            temp['is_liked_by_curr_user'] = True

        temp['comments'] = post['comments']
        temp['description'] = post['description']
        photo= post["image"].grid_id
        col = db.images.chunks.find({"files_id":photo})
        my_string = base64.b64encode(col[0]["data"])
        temp["photo"] = my_string.decode('utf-8')
        temp["owner_photo"] = my_string1.decode('utf-8')
        clan_posts.append(temp)



    #print(clan)
    return render(request, 'clans/clan_show.html', {'clan_challenges_today':clan_challenges_today,'clan_members':clan_members,'clan_posts':clan_posts, "clan_id":clan_id,'is_head':is_head , 'clan_challenges':clan_challenges})


@login_required
def add_clan_user(request, clan_id):
    ae,user=check_user_exists(request,request.session["username"])
    profile = Profile.objects.get(id = user["profileid"])
    content=list()
    for h in User.objects.all()[:16]:
        if h["id"] == user["id"]:
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
    return render(request, 'clans/clan_add_user.html',{"content":content, "clan_id":clan_id})


def search(request):
    print("clan search")
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
    return render_to_response('clans/li.html',{"content":content})


def add_user(request):
    if request.method=='POST':
        ad_user = request.session["username"]
        username = request.POST['uid']
        clanid = request.POST['clan_id']
        a_uid = User.objects(email=ad_user)[0]
        a_uid_prof = Profile.objects(user_id=a_uid['id'])[0]
        uid = User.objects(email=username)[0]
        uid_prof = Profile.objects(user_id=uid['id'])[0]
        clan = community.objects(id=clanid)[0]

        flag = False
        members = clan.participants
        if uid["id"] in members:
            print("User already in group")
            return HttpResponse('User already in group')
        else:
            Profile.objects(user_id=uid["id"]).update_one(push__clans_registered=clanid)
            print("Profile Updated")
            community.objects(id=clanid).update_one(push__participants=uid["id"])
            print("Clan Participant Added")
            community.objects(id=clanid).update_one(set__no_of_participants=clan.no_of_participants+1)
            print("clan num participants changed")
            text = a_uid_prof.name
            text += " added " 
            text += uid_prof.name
            print("Message: ", text)
            message = GroupMessage(msg=text,sender=a_uid['id'],group=clanid)
            message.save()
            print("message saved")
            print(message['id'])
            community.objects(id=clanid).update_one(push__messages = message['id'])
            return HttpResponse('User added into group')


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



@login_required
def single_post(request):
    if request.method == "GET":
        print("came into single_post")
        post_id = request.GET["postId"]

        username = request.session["username"]
        user = User.objects(email=username)[0]
        profile = Profile.objects.get(user_id=user["id"])

        temp = dict()
        post = Post.objects.get(id = post_id)
        temp['id'] = post['id']
        po = post['owner']
        po_p = Profile.objects.get(user_id = po)
        temp['owner'] = po_p['name']

        temp['createdAt'] = post['createdAt']
        temp['likes'] = post['likes']
        temp['likedBy'] = post['likedBy']
        temp['is_liked_by_curr_user'] = False

        if user['id'] in post['likedBy']:
            temp['is_liked_by_curr_user'] = True

        temp['comments'] = post['comments']
        temp['description'] = post['description']
        photo= post["image"].grid_id
        col = db.images.chunks.find({"files_id":photo})
        my_string = base64.b64encode(col[0]["data"])
        temp["photo"] = my_string.decode('utf-8')
        # temp["owner_photo"] = my_string1.decode('utf-8')
        o_photo= po_p["photo"].grid_id
        o_col = db.images.chunks.find({"files_id":o_photo})
        o_my_string = base64.b64encode(o_col[0]["data"])
        temp["ownerphoto"] = o_my_string.decode('utf-8')

        my_photo= profile["photo"].grid_id
        my_col = db.images.chunks.find({"files_id":my_photo})
        my_my_string = base64.b64encode(my_col[0]["data"])
        temp["ownerphoto"] = my_my_string.decode('utf-8')
        


        

        comments = []
        


        for k in post['comments']:
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
        print(count)
        return render(request, 'clans/modal.html', {'myphoto': my_photo,'post': temp, 'comments': comments, 'count': count})
    else:
        return HttpResponse("failure")


def getComments(request):
    if request.method == 'GET':
        post_id = request.GET['postId']
        username = request.session["username"]
        user = User.objects(email=username)[0]
        profile = Profile.objects.get(user_id=user["id"])

        post = Post.objects.get(id = post_id)

        comments = []
        


        for k in post['comments']:
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
        print(count)
        return render('clans/comments.html', {'comments': comments, 'count':count})

def like(request):
    if request.method == 'GET':
        post_id = request.GET['postId']
        username = request.session["username"]
        user = User.objects(email=username)[0]
        profile = Profile.objects.get(user_id=user["id"])
        post = Post.objects.get(id = post_id)

        if user['id'] not in post['likedBy']:
            post.likes += 1
            post.likedBy.append(user["id"])
            post.save()
        else:
            post.likes -= 1
            post.likedBy.remove(user["id"])
            post.save()
        return HttpResponse('Success')
    else:
        return HttpResponse(Failure)






        

