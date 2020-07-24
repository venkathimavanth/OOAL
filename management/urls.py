from django.urls import path,include
from . import views

app_name = "management"

urlpatterns = [
    path('addchallenge/', views.addchallenge ,name='addchallenge'),
    path('managementhome/', views.managementhome ,name='managementhome'),
    path('dailychallanges/', views.dailychallanges ,name='dailychallanges'),
    # path('temp/', views.temp ,name='temp'),
    path('find/prev/', views.findprev ,name='findprev'),
    path('find/next/', views.findnext ,name='findnext'),
    path('addcatogries', views.addcatogries ,name='addcatogries'),
    path('fun_upload/', views.fun_upload,name='fun_upload'),
    path('addweeklychallenge/', views.addweeklychallenge ,name='addweeklychallenge'),


]
