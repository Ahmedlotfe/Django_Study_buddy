from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('update-profile/', views.updateProfile, name='update-profile')
]
