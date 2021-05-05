from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

#Incorporate a new API "Facebook App - sends your ranking/awards as a post on facebook"

#Create a field for badges
class Profile(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    age = models.DecimalField(decimal_places=0, max_digits=2)
    height = models.FloatField()
    level = models.DecimalField(decimal_places=0, max_digits=2)
    email = models.CharField(max_length=100)
    ThumbsUp = models.IntegerField(default=0)
    def __str__(self):
        return self.name

#Gameifications Badges, Points
class Dashboard(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Friends = ArrayField(models.CharField(max_length=30))
    Workout = ArrayField(models.CharField(max_length=100))
    def __str__(self):
        return self.User.username

class Workouts(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Workout_Name = ArrayField(models.CharField(max_length=100))
    Workout_Progress = ArrayField(models.DecimalField(decimal_places=0, max_digits=4))
    Workout_Goals = ArrayField(models.DecimalField(decimal_places=0, max_digits=4))
    def __str__(self):
        return self.User.username
