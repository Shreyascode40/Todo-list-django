from django.contrib import admin
from django.urls import path
from django.urls import include
from account import views

app_name = 'account'

urlpatterns = [
    path('register/',views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    
]
