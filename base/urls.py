from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns= [
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('add_room', views.createRoom, name='add_room'),
    path('update_room/<str:pk>/', views.updateRoom, name='update_room'),
    path('delete_room/<str:pk>/', views.roomDelete, name= 'delete_room'),
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('delete_message/<str:pk>/', views.DeleteMessage, name= 'delete_message'),
    path('profile/<str:pk>/', views.userProfile, name= 'profile'),
    path('logout/', views.logoutUser, name='logout'),
    path('update_profile/', views.updateUser, name= 'update_profile'),
    path('topics/', views.topicPage, name= 'topics'),
    path('activity/', views.activityPage, name= 'activity'),


]