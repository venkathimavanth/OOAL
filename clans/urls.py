from django.conf.urls import url
from django.urls import path,include
from . import views

app_name = "community"

urlpatterns = [
    path('create_clan/', views.create_clan ,name='create-clan'),
    path('clans/', views.clanHome ,name='clan-home'),
    path('clan/<clan_id>', views.clan_show, name='clan-show'),
    path('clan/like/<post_id>', views.like_post, name='clan-like'),
    path('clan/unlike/<post_id>', views.unlike_post, name='clan-unlike'),
    path('clan/post/<clan_id>', views.post, name='clan-post'),
    path('clan/adduser/<clan_id>', views.add_clan_user, name='add-clan-user'),
    path('clan/add/user', views.add_user, name='add-user'),
    path('clan/search/', views.search, name='search'),
    #url(r'^likepost/$', views.likePost, name='likepost')
]
