from django.urls import path,include
from . import views

app_name = "community"

urlpatterns = [
    path('create_clan/', views.create_clan ,name='create-clan'),
    path('clans/', views.clanHome ,name='clan-home'),
    path('clan/<clan_id>', views.clan_show, name='clan-show'),
    path('clan/adduser/<clan_id>', views.add_clan_user, name='add-clan-user'),
    path('clan/add/user', views.add_user, name='add-user'),
    path('clan/search/', views.search, name='search'),
    path('createclan/', views.create_clan ,name='create_clan'),
    path('add_participants/<slug:slug>/', views.add_participants ,name='add_participants'),
    #path('clanshome/', views.clanshome ,name='clanshome'),

]
