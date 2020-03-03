from django.urls import path,include
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

]
