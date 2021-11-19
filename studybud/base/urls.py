from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('room/<int:pk>/', views.room, name='room'),

    path('create-room/', views.createRoom, name='create-room'),

    path('room/<int:pk>/update/', views.updateRoom, name='update-room'),

    path('room/<int:pk>/delete/', views.deleteRoom, name='delete-room'),

    path('room-message/<int:pk>/', views.deleteRoomMessage,
         name='delete-room-message'),

    path('topics/', views.topicPage, name='topics'),

    path('activity/', views.activityPage, name='activity'),
]
