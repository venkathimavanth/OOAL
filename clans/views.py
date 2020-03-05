from user_auth.models import User,Profile
import datetime,bcrypt,hashlib
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from user_auth.decorators import login_required,management_required
from django.core.mail import EmailMessage, send_mail
from rest_framework.views import APIView
from .models import community

# Create your views here.

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