from django.urls import path,include
from authuser.views import UserLogin,UserRegistration
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('register',UserRegistration.as_view(),name='register'),
    path('login',UserLogin.as_view(),name='login'),
    path('logout',LogoutView.as_view(next_page='login'),name='logout'),
]