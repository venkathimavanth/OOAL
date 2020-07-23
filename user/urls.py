from django.urls import path,include,re_path
from . import views

app_name = "user"

urlpatterns = [
    # path('addchallenge/', views.addchallenge ,name='addchallenge'),
    path('viewprofile/<email>/', views.viewprofile ,name='viewprofile'),
    path('viewprofile/<email>/<test>/', views.friend_req_handle ,name='friend_req_handle'),
    path('friends/', views.friends ,name='friends'),
    path('pendingrequests/', views.pendingrequests ,name='pendingrequests'),
    path('findfriends/', views.findfriends ,name='findfriends'),
    path('pendingrequests/<email>/', views.viewfullprofile ,name='viewfullprofile'),
    path('pendingrequests/<email>/<type>/', views.add_deop_req ,name='add_deop_req'),
    path('friends/<email>/', views.viewfullprofile ,name='viewfullprofile'),
    path('findfriends/<email>/', views.viewfullprofile ,name='viewfullprofile'),
    path('userhome/viewprofile/<email>/', views.viewfullprofile ,name='viewfullprofile'),
    path('articles/search/', views.autocompleteModel,name="autocompleteModel"),
    path('viewmyprofile/', views.viewmyprofile ,name='viewmyprofile'),
    path('challanges/', views.challanges ,name='challanges'),
    path('userhome/', views.userhome ,name='userhome'),
    path('challange/dsc/', views.dsc ,name='dsc'),

]
