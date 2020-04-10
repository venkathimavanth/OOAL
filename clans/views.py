from user_auth.models import User,Profile
import datetime,bcrypt,hashlib
from django.shortcuts import render,redirect, render_to_response, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from user_auth.decorators import login_required,management_required
from user_auth.views import check_user_exists
from django.core.mail import EmailMessage, send_mail
from rest_framework.views import APIView
from .models import community
from chat.models import Message, GroupMessage


import base64
import datetime,json

# Create your views here.

# import the MongoClient class from the library
from pymongo import MongoClient
mongo_client = MongoClient()
db = mongo_client.EAD_OOAL


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
    username = request.session["username"]
    user = User.objects(email=username)[0]
    profile = Profile.objects(user_id=user["id"])[0]
    clans = []
    for i in profile["clans_registered"]:
        clan = community.objects(id=i)
        clans.append(clan)
    print(clans)
    
    return render(request,'clans/clans.html',{"clans": clans, "username": profile["name"]})

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


def search(request):
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
        return HttpResponse('')
        
        


