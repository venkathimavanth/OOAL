from django.http import HttpResponse
from django.shortcuts import redirect
from user_auth.models import User


def login_required(func):
    def wrap_func(request,*args,**kwargs):
        print("called login_required dec func")
        # print(request.session.has_key('username'))
        if not request.session.has_key('username'):
            return redirect('user_auth:login')
        elif request.session.has_key('username'):
            us=User.objects.filter(email=request.session['username'])
            if us:
                u=None
                for u in us:
                    pass
                if u["email_verified"]:
                    if u["user_type"] == "0" :
                        if u["profile_created"]:
                            return func(request,*args,**kwargs)
                        else:
                            return redirect("user_auth:create_profile")
                    if request.session.has_key('username'):
                        print("logoutd1")
                        try:
                            del request.session["username"]
                        except:
                            pass
                    return redirect('user_auth:login')
                else:
                    if request.session.has_key('username'):
                        print("logout")
                        print("logoutd1")
                        try:
                            del request.session["username"]
                        except:
                            pass
                    return redirect('user_auth:verify_email')
            else:
                if request.session.has_key('username'):
                    print("logout")
                    print("logoutd1")
                    try:
                        del request.session["username"]
                    except:
                        pass
                return redirect('user_auth:login')

        else:
            return func(request,*args,**kwargs)

    return wrap_func

def management_required(func):
    print("called management_required dec func")
    def wrap_func(request,*args,**kwargs):
        if not request.session.has_key('username'):
            return redirect('user_auth:login')
        elif request.session.has_key('username'):

            us=User.objects.filter(email=request.session['username'])
            if us:
                u=None
                for u in us:
                    pass
                if u["email_verified"]:
                    if u["user_type"] == "1" :
                        return func(request,*args,**kwargs)
                    if request.session.has_key('username'):
                        print("logoutd1")
                        try:
                            del request.session["username"]
                        except:
                            pass
                    return redirect('user_auth:login')
                else:
                    if request.session.has_key('username'):
                        print("logoutd1")
                        try:
                            del request.session["username"]
                        except:
                            pass
                    return redirect('user_auth:verify_email')
            else:
                if request.session.has_key('username'):
                    print("logoutd1")
                    try:
                        del request.session["username"]
                    except:
                        pass
                return redirect('user_auth:login')

        else:
            return func(request,*args,**kwargs)

    return wrap_func
