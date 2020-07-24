from django.shortcuts import render, HttpResponse
from user_auth.decorators import login_required,management_required
from user_auth.models import User,Profile
from clans.models import community
from .models import Message, GroupMessage

import base64
import datetime,json

# Create your views here.

# import the MongoClient class from the library
from pymongo import MongoClient
mongo_client = MongoClient()
db = mongo_client.EAD_OOAL


@login_required
def chatHome(request):
    username = request.session["username"]
    user = User.objects(email=username)[0]
    profile = Profile.objects(user_id=user["id"])[0]
    frnds = profile.friends
    clans = profile.clans_registered
    friends_list = []
    groups_list = []
    for friend in frnds:
        temp = dict()
        frnd = Profile.objects(user_id=friend)[0]
        frnd_u = User.objects(id=friend)[0]
        temp['name'] = frnd["name"]
        temp['id'] = frnd_u["id"]
        photo= frnd["photo"].grid_id
        col = db.images.chunks.find({"files_id":photo})
        my_string = base64.b64encode(col[0]["data"])
        temp["photo"] = my_string.decode('utf-8')
        friends_list.append(temp)
    print(len(friends_list))
    for clan in clans:
        temp = dict()
        group = community.objects(id=clan)[0]
        temp["id"] = group["id"]
        temp['name'] = group["name"]
        photo= group["photo"].grid_id
        col = db.images.chunks.find({"files_id":photo})
        my_string = base64.b64encode(col[0]["data"])
        temp["photo"] = my_string.decode('utf-8')
        groups_list.append(temp)
    print(len(groups_list))
    return render(request,'chat/home.html',{'friends_list': friends_list, 'groups_list': groups_list})

@login_required
def getMsgs(request):
    if request.method=="GET":
        chat_msgs = []
        friend_id = request.GET['f_id']
        cu_user = request.session["username"]
        c_user = User.objects(email=cu_user)[0]
        c_u_prof = Profile.objects(user_id=c_user['id'])[0]
        msgs = c_u_prof['messages']

        if(msgs):
            for msg in msgs:
                c_msg = Message.objects(id=msg)[0]
                if c_msg['sender'] == friend_id:
                    chat_msgs.append(c_msg)


    return render(request,'chat/priv_msg.html')

@login_required
def getGroupMsgs(request):
    if request.method=="GET":
        group_msgs = []
        group_id = request.GET['clan_id']
        print("Group Id : ",group_id)
        cu_user = request.session["username"]
        c_user = User.objects(email=cu_user)[0]
        uid = c_user['id']
        clan = community.objects(id=group_id)[0]
        print("got clan object")
        temp = dict()
        temp['id'] = clan["id"]
        temp['name'] = clan["name"]
        photo= clan["photo"].grid_id
        col = db.images.chunks.find({"files_id":photo})
        my_string = base64.b64encode(col[0]["data"])
        temp["photo"] = my_string.decode('utf-8')
        group_details = temp

        msgs = clan['messages']
        for msg in msgs:
            print(msg)
            g_msg = GroupMessage.objects(id=msg)[0]
            group_msgs.append(g_msg)
    return render(request,'chat/msg.html', {'group_msgs': group_msgs, "group_details": group_details, "uid":uid})


@login_required
def sendGrpMsg(request):
    if request.method =='POST':
        text = request.POST['msg']
        c_id = request.POST['clan_id']
        cu_user = request.session["username"]
        c_user = User.objects(email=cu_user)[0]
        c_u_prof = Profile.objects(user_id=c_user['id'])[0]
        message = GroupMessage(msg=text,sender=c_user['id'],group=c_id)
        message.save()
        print("message saved")
        print(message['id'])
        community.objects(id=c_id).update_one(push__messages = message['id'])
        return HttpResponse('Success')
    else:
        return HttpResponse('Failure')



def getPrivMsgs(request):
    if request.method == 'GET':
        frnd_id = request.GET['f_id']

        cu_user = request.session["username"]
        c_user = User.objects(email = cu_user)[0]
        cu_prof = Profile.objects.get(user_id = c_user['id'])
        frnd_prof = Profile.objects.get(user_id = frnd_id)
        my_id = c_user['id']
        frnd_name = frnd_prof['name']

        myphoto= cu_prof["photo"].grid_id
        mycol = db.images.chunks.find({"files_id":myphoto})
        myph = base64.b64encode(mycol[0]["data"])
        my_photo = myph.decode('utf-8')
        frndphoto= frnd_prof["photo"].grid_id
        frndcol = db.images.chunks.find({"files_id":frndphoto})
        frndph = base64.b64encode(frndcol[0]["data"])
        frnd_photo = frndph.decode('utf-8')


        msgs = cu_prof['messages']
        print('Profile msgs', len(msgs))
        messages = []

        for msg in msgs:
            print(msg)
            temp = Message.objects.get(id = msg)
            temp_r = temp['reciever']
            temp_s = temp['sender']
            ff_id = frnd_prof['user_id']
            print(temp_r == ff_id)
            print(temp_s == ff_id)
            if temp_s == ff_id or temp_r == ff_id:
                temp1 = dict()
                temp1['message'] = temp['msg']
                temp1['sender'] = temp['sender']
                temp1['reciever'] = temp['reciever']
                temp1['time'] = temp['createdAt']

                messages.append(temp1)
            else:
                continue
        
        print('messages',len(messages))
        print('frnd', frnd_name)
        
        return render(request, 'chat/priv_msg.html', {'messages': messages, "friend": frnd_name ,"my_id":my_id, "my_photo":my_photo, "frnd_photo": frnd_photo, "friend_id": frnd_id})
    else:
        return HttpResponse('Failure')
    
def sendPrivMsg(request):
    if request.method == 'POST':
        print("got request")
        text = request.POST['msg']
        frnd_id = request.POST['f_id']
        print(text)
        print(frnd_id)

        cu_user = request.session["username"]
        c_user = User.objects(email = cu_user)[0]
        cu_prof = Profile.objects.get(user_id = c_user['id'])
        
        msg = Message(msg=text, sender=c_user['id'], reciever=frnd_id)
        msg.save()
        print("message saved")

        Profile.objects(user_id = c_user['id']).update_one(push__messages = msg['id'])
        Profile.objects(user_id = frnd_id).update_one(push__messages = msg['id'])
        print("Profiles changed")
        return HttpResponse('Success')
    else:
        return HttpResponse('Failure')
