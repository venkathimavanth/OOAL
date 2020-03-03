from django.urls import path,include
from . import views

app_name = "user_auth"

urlpatterns = [
    path('', views.home ,name='home'),
    path('signup/', views.signup ,name='signup'),
    path('login/', views.login ,name='login'),
    path('loggedinhome/', views.loggedinhome ,name='loggedinhome'),
    path('logout/', views.logout ,name='logout'),
    path('verify_email/', views.verify_email ,name='verify_email'),
    path('email_verified/<email>/<hash>/', views.email_verified ,name='email_verified'),
    path('forgot_password/', views.forgot_password ,name='forgot_password'),
    path('change_password/<email>/<hash>/', views.change_password ,name='change_password'),
    path('managementhome/', views.managementhome ,name='managementhome'),
    path('create_profile/', views.create_profile ,name='create_profile'),


]
