from user_auth.models import User,Profile
import datetime,bcrypt,hashlib
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .decorators import login_required,management_required,business_required
from django.core.mail import EmailMessage, send_mail
from rest_framework.views import APIView

# Create your views here.
def home(request):
    print("called home view func")
    if request.method=='GET':
        r=check_loggedin(request)
        if r:
            return r
    return render(request,'home.html')

def check_user_exists(request,name):
    for u in User.objects.all():
        if u["email"] == name:
            return (True,u)
    return (False,None)


def check_loggedin(request):
    if request.session.has_key('username'):
        e,u = check_user_exists(request,request.session["username"])
        if e:
            if u["user_type"] == "1":
                return redirect('user_auth:managementhome')
            elif u["user_type"] == "2":
                return redirect('user_auth:businesshome')
            return redirect('user_auth:loggedinhome')
        else:
            print("logout1")
            try:
                del request.session["username"]
            except:
                pass
    return False

def signup(request):
    print("called signup view func")
    if request.method=='GET':
        r=check_loggedin(request)
        if r:
            return r
    elif request.method=='POST':
        if "name" in request.POST and "password" in request.POST and "repassword" in request.POST  :
            if request.POST["password"] == request.POST["repassword"]:
                if not check_user_exists(request,request.POST["name"])[0]:#check unique user or not
                    mail_subject = 'Activate your OOAL account.'
                    mail=str(request.POST["name"]).encode("utf-8")
                    hashed = bcrypt.hashpw(mail,bcrypt.gensalt())
                    hashed = hashed.decode('ascii')
                    temp=""
                    for h in hashed:
                        temp += str(ord(h)) + '_'
                    hashed=temp
                    message = str("Please click the link below \n\n") + "http://127.0.0.1:8000/email_verified" + "/" + str(request.POST["name"]) + "/"+ hashed
                    to_email = request.POST["name"]
                    email = EmailMessage(
                                mail_subject, message, to=[request.POST["name"]]
                                )
                    email.send()

                    password=str(request.POST["password"]).encode("utf-8")
                    hashed = bcrypt.hashpw(password,bcrypt.gensalt())
                    hashed=hashed.decode('ascii')
                    user = User(email=request.POST["name"], password=hashed,created_date=datetime.datetime.now(),user_type="0")
                    user.save()
                    #request.session['username'] = request.POST["name"]
                    return verify_email(request)
                else:
                    return render(request,'registration/signup.html',{'warning':"User alderady exist"})
            else:
                return render(request,'registration/signup.html',{'warning':"Password dosent match"})
        else:
            return render(request,'registration/signup.html',{'warning':"Fill all elements"})
    return render(request,'registration/signup.html',{'warning':""})

def login(request):
    print("called login view func")
    if request.method=='GET':
        r=check_loggedin(request)
        if r:
            return r
    elif request.method=='POST':
        if "name" in request.POST and "password" in request.POST   :
            e,u = check_user_exists(request,request.POST["name"])
            if e:
                password=str(request.POST["password"]).encode("utf-8")
                if bcrypt.checkpw( password , u["password"].encode("utf-8") ) :
                    request.session['username'] = request.POST["name"]
                    if u["user_type"] == "1":
                        return redirect('user_auth:managementhome')
                    if u["user_type"] == "2":
                        return redirect('user_auth:businesshome')

                    return redirect('user_auth:loggedinhome')
                else:
                    return render(request,'registration/login.html',{'warning':"Incorrect Password"})
            else:
                return render(request,'registration/login.html',{'warning':"User dosent exist"})
        else:
            return render(request,'registration/login.html',{'warning':"Fill all elements"})
    return render(request,'registration/login.html',{})

# @login_required
def loggedinhome(request):
    print("called loggedinhome view func")
    return redirect('user:userhome')
    # return render(request,'registration/loginhome.html',{'warning':"Logged in successfully"})


@management_required
def managementhome(request):
    print("called managementhome view func")
    return render(request,'management/managementhome.html',{'warning':"Logged in successfully"})

@business_required
def businesshome(request):
    print("called businesshome view func")
    return render(request,'business/businesshome.html',{'warning':"Logged in successfully"})

@login_required
def logout(request):
    print("called logout view func")
    if request.session.has_key('username'):
        print("logout4")
        try:
            del request.session["username"]
        except:
            pass
    return redirect('user_auth:home')

def verify_email(request):
    return render(request,'registration/verify_email.html',{})


def forgot_password(request):
    print("called forgot_password view func")
    if request.method == 'GET':
        return render(request,'registration/forgot_password.html',{})
    elif request.method == 'POST':
        if "name" in request.POST:
            e,u = check_user_exists(request,request.POST["name"])
            if e:
                mail_subject="Chnage your password"
                mail=str(request.POST["name"]).encode("utf-8")
                hashed = bcrypt.hashpw(mail,bcrypt.gensalt())
                hashed = hashed.decode('ascii')
                temp=""
                for h in hashed:
                    temp += str(ord(h)) + '_'
                hashed=temp
                message = str("Please click the link below \n\n") + "http://127.0.0.1:8000/change_password" + "/" + str(request.POST["name"]) + "/"+ hashed
                to_email = [request.POST["name"],]
                # print(mail_subject,message,to_email)
                send_mail_func(request,mail_subject,message,to_email)
                return render(request,'registration/change_password_msg.html',{})
            else:
                return render(request,'registration/forgot_password.html',{"warning":"Account dosen't exists"})
    return render(request,'registration/forgot_password.html',{})


def change_password(request,email,hash):
    print("called change_password view func")
    if request.method == 'GET':
        mail=str(email).encode("utf-8")
        hash=hash[:len(hash)-1]
        hash=hash.split('_')
        temp=""
        for h in hash:
            try:
                temp += chr(int(h))
            except:
                return render(request,'home.html')
        hash=temp
        if bcrypt.checkpw( mail , hash.encode("utf-8") ):
            e,u=check_user_exists(request,email)
            if e:
                u["email_verified"] = True
                u.save()
                request.session['username'] = email
                return render(request,'registration/change_password.html',{})
            else:
                return render(request,'home.html')
        else:
            return render(request,'home.html')

    if request.method == 'POST':
        if "password" in request.POST and "repassword" in request.POST :
            if request.POST["password"] == request.POST["repassword"] :
                if request.session.has_key('username'):
                    e,user = check_user_exists(request,request.session["username"])
                    if e :
                        password=str(request.POST["password"]).encode("utf-8")
                        hashed = bcrypt.hashpw(password,bcrypt.gensalt())
                        hashed=hashed.decode('ascii')
                        user["password"] = str(hashed)
                        user.save()
                        request.session["username"] = user["email"]
                        return loggedinhome(request)
                print("logout5")
                try:
                    del request.session["username"]
                except:
                    pass
                return render(request,'home.html')
            else:
                return render(request,'registration/change_password.html',{"Warning":"Passwords dosen't match"})
        else:
            return render(request,'registration/change_password.html',{"Warning":"Please fill all the elements"})
    return render(request,'home.html')

def email_verified(request,email,hash):
    print("called email_verified view func")
    if request.method == 'GET':
        mail=str(email).encode("utf-8")
        hash=hash[:len(hash)-1]
        hash=hash.split('_')
        temp=""
        for h in hash:
            try:
                temp += chr(int(h))
            except:
                return render(request,'home.html')
        hash=temp
        if bcrypt.checkpw( mail , hash.encode("utf-8") ):
            e,u=check_user_exists(request,email)
            if e:
                u["email_verified"] = True
                u.save()
                request.session['username'] = email
                return redirect("user_auth:loggedinhome")
            else:
                return render(request,'home.html')
        else:
            return render(request,'home.html')
    return render(request,'home.html')

def send_mail_func(request,mail_subject,message,to_email):
    email = EmailMessage(
                mail_subject, message, to=to_email
                )
    email.send()
    return


def create_profile(request):
    print("called create_profile view func")
    if request.method == 'GET':
        if request.session.has_key('username') and User.objects.filter(email=request.session['username']):
            if User.objects.get(email=request.session['username'])["profile_created"]:
                return redirect('user_auth:loggedinhome')
            return render(request,'registration/create_profile.html',{"warning":""})
        try:
            del request.session["username"]
        except:
            pass
        return redirect('user_auth:login')
    if request.method == 'POST':
        if request.session.has_key('username'):
            e,u = check_user_exists(request,request.session["username"])
            if not e:
                try:
                    del request.session["username"]
                except:
                    pass
                return redirect('user_auth:login')
            if "age" in request.POST and "city" in request.POST and "country" in request.POST  and "photo" in request.FILES and "name" in request.POST and "discription" in request.POST:
                parental_account=False
                parental_password=""
                if "parental_account" in request.POST:
                    parental_account = request.POST["parental_account"]
                    parental_password = request.POST["parental_password"]

                user_id = u["id"]
                name = request.POST["name"]

                photo=request.FILES["photo"]
                discription = request.POST["discription"]
                age = int(request.POST["age"])
                city = request.POST["city"]
                country = request.POST["country"]
                prof=Profile(name=name,discription=discription,user_id=user_id,age=age,city=city,country=country,parental_account=parental_account,parental_password=parental_password).save()
                prof.photo.put(photo, content_type = 'image/jpeg')
                prof.save()
                u["profile_created"] = True
                u["profileid"] = prof["id"]
                u.save()
                return redirect('user_auth:loggedinhome')
            else:
                return render(request,'registration/create_profile.html',{"warning":"Please fill all the blanks"})
    return redirect('user_auth:login')
