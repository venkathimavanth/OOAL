import clans
from user_auth.models import User,Profile
import datetime,bcrypt,hashlib
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from user_auth.decorators import login_required,management_required
from django.core.mail import EmailMessage, send_mail
from rest_framework.views import APIView
<<<<<<< Updated upstream
from .models import community

# Create your views here.

=======
from .models import community,Post
from chat.models import Message, GroupMessage


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



>>>>>>> Stashed changes
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
def clanHome(request):
    print('I am in clan home')
    username = request.session["username"]
<<<<<<< Updated upstream
    user = User.objects(email=username)[0]
    profile = Profile.objects(user_id=user["id"])[0]
    print(profile)
    clans = []

=======
    user = User.objects.get(email=username)
    profile = Profile.objects.get(user_id=user["id"])
    clans1 = []
>>>>>>> Stashed changes
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


<<<<<<< Updated upstream
=======
@login_required
def clan_show(request, clan_id):
    username = request.session["username"]
    user = User.objects(email=username)[0]
    profile = Profile.objects.get(user_id=user["id"])
    clan = community.objects.get(id=clan_id)
    clan_id = clan['id']
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
    return render(request, 'clans/clan_show.html', {'clan_members':clan_members,'clan_posts':clan_posts, "clan_id":clan_id})


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
>>>>>>> Stashed changes

def add_participants(request,slug):
    if request.method == 'POST':
                id = request.POST["users"]
                print(id)
                Profile.objects(id = id).update_one(push__pending_clan_requests = slug)

<<<<<<< Updated upstream
                return redirect('user_auth:loggedinhome')
    else:
            prof = Profile.objects.all()
            return render(request, 'clans/add_participant.html', {'prof': prof, "warning":"Please fill all the blanks"})
=======
def search(request):
    print("clan search")
    if request.method == "POST":
        search_text= request.POST['search_text']
    else:
        search_text=""

    print(Profile.objects.filter(name__startswith=search_text)[:16])
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

>>>>>>> Stashed changes
