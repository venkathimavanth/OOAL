from django.urls import path,include
from . import views


app_name = "chat"

urlpatterns = [
    path('chat/', views.chatHome, name='chat-home'),
    path('chat/send/<rec_id>', views.sendMsg, name='send-msg-private'),
]
