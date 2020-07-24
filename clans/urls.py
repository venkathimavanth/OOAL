from django.conf.urls import url
from django.urls import path,include
from . import views

app_name = "community"

urlpatterns = [
    path('create_clan/', views.create_clan ,name='create-clan'),
    path('clans/', views.clanHome ,name='clan-home'),
    path('clans/temp', views.temp ,name='clan-temp'),
    path('clan/<clan_id>', views.clan_show, name='clan-show'),
    path('clan/show_challanges/<clan_id>', views.show_challanges, name='show_challanges'),
    path('clan/review_challanges/<clan_id>', views.review_challanges, name='review_challanges'),
    path('clan/accept_challange/<chall_id>', views.accept_challange, name='accept_challange'),
    path('clan/reject_challange/<chall_id>', views.reject_challange, name='reject_challange'),
    path('clan/submit_challanges/<challange_id>', views.submit_challanges, name='submit_challanges'),
    path('clan/submit_form/<challange_id>', views.submit_form, name='submit_form'),
    path('clan/add_challange/<clan_id>', views.add_challange, name='add_challange'),
    path('clan/adduser/<clan_id>', views.add_clan_user, name='add-clan-user'),
    path('clan/add/user', views.add_user, name='add-user'),
    path('clan/search/', views.search, name='search'),
    path('clan/like/<post_id>', views.like_post, name='clan-like'),
    path('clan/unlike/<post_id>', views.unlike_post, name='clan-unlike'),
    path('clan/post/<clan_id>', views.post, name='clan-post'),
    path('clan/post/comment/', views.createComment, name='post-comment'),
    path('clan/post/single/', views.single_post, name='modal-post'),
    path('clan/post/getcomments/', views.getComments, name='get-comments'),
    path('clan/post/like/', views.like, name='modal-like-post'),
    path('clan/exit/<clan_id>', views.exitClan, name='exit-clan'),
    #url(r'^likepost/$', views.likePost, name='likepost')
]
