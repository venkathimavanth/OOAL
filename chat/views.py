from django.shortcuts import render
from user_auth.decorators import login_required,management_required
from user_auth.models import User,Profile

# Create your views here.

@login_required
def chatHome(request):
    username = request.session["username"]
    user = User.objects(email=username)[0]
    profile = Profile.objects(user_id=user["id"])[0]
    users = User.objects(email=username)
    print(users)
    users.remove(user)
    print(users)
    return render(request,'chat/home.html')

@login_required
def sendMsg(request):
    if request.method =='POST':
        msg = request.POST['msg']
        rec_id = request.POST['']
