from django.urls import path
from django.contrib.auth.models import User
from . import views

app_name = 'social_app'
urlpatterns = [
        path('<str:email>', views.ProfilePage, name = 'profile'),
        path('<str:email>/dashboard', views.DashboardPage, name = 'dashboard'),
        path('<str:email>/Workout', views.WorkoutPage, name = 'workout'),
        path('<str:email>/dashboard/AddFriends', views.AddFriends, name = 'AddFriends'),
        path('<str:email>/dashboard/AddWorkout', views.AddWorkout, name = 'AddWorkout'),
        path('<str:email>/dashboard/UpdateWorkout', views.UpdateWorkout, name = 'UpdateWorkout'),
        path('<str:email>/dashboard/<str:name>', views.FriendPage, name = 'friendpage'),
]