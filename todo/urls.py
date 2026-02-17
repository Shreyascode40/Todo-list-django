from django.contrib import admin
from django.urls import path
from django.urls import include

from todo import views
app_name = 'todo'


urlpatterns = [
    path('',views.todo_list, name='todo_list'),
    path('create/',views.todo_create, name='todo_create'),
    path('update/<int:pk>/',views.todo_update, name='todo_update'),
    path('delete/<int:pk>/',views.todo_delete, name='todo_delete'),
    path('todo/complete/<int:pk>/',views.todo_complete, name='todo_complete'),
    path('tracker/',views.tracker_view,name='tracker'),
]
