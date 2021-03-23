from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=30)
    age = models.DecimalField(decimal_places=0, max_digits=2)
    height = models.DecimalField(decimal_places=0, max_digits=1)
    time = models.DecimalField(decimal_places=0, max_digits=4)
    email = models.CharField(max_length=100)
    def __str__(self):
        return self.name
