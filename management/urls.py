from django.urls import path,include
from . import views

app_name = "management"

urlpatterns = [
    path('addchallenge/', views.addchallenge ,name='addchallenge'),
]
