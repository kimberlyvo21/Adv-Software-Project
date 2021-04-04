from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.json import JSONField

class Profile(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    age = models.DecimalField(decimal_places=0, max_digits=2)
    height = models.DecimalField(decimal_places=0, max_digits=1)
    time = models.DecimalField(decimal_places=0, max_digits=4)
    email = models.CharField(max_length=100)
    def __str__(self):
        return self.name

#Gameifications Badges, Points
class Dashboard(models.Models):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Freinds = JSONField()
    #WorkOutGoals
    CurrGoal = models.DecimalField(decimal_places=0, max_digits=4)
