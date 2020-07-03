from django.urls import path,include
from . import views


app_name = "chat"

urlpatterns = [
    path('chat/', views.chatHome, name='chat-home'),
    path('chat/sendGrpMsg/', views.sendGrpMsg, name='send-msg-group'),
    path('chat/getMsg/', views.getMsgs, name='get-msg-private'),
    path('chat/getGrpMsg/', views.getGroupMsgs, name='get-grp-msg'),
]
