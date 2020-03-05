from django.urls import path,include
from . import views

app_name = "community"

urlpatterns = [
    path('create_clan/', views.create_clan ,name='create-clan'),
    path('clans/', views.clanHome ,name='clan-home'),
    path('createclan/', views.create_clan ,name='create_clan'),
    path('add_participants/<slug:slug>/', views.add_participants ,name='add_participants'),
    #path('clanshome/', views.clanshome ,name='clanshome'),

]
