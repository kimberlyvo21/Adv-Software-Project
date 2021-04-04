from django.urls import path
from django.contrib.auth.models import User
from . import views

app_name = 'social_app'
urlpatterns = [
        path('<str:email>', views.ProfilePage, name = 'profile'),
        path('<str:email>/dashboard', views.Dashboard, name = 'dashboard',)
]