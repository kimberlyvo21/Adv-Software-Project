from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User
# Create your tests here.


def create_account(username, age, height, workout_time):
    User.objects.create_user(username=username, email="John@gmail.com")
    return Profile.objects.create(User=User.objects.get(username=username), name="John Doe", age=age, height=height, time=workout_time,
                                  email="John@gmail.com")


class ProfileCreation(TestCase):
    def test_case_profile_accept(self):
        new_user = create_account("James", 18, 6, 60)
        all_users = User.objects.all()
        self.assertQuerysetEqual(all_users, ['<User: James>'])

    def test_case_profile_more_than_one(self):
        new_user = create_account("James", 18, 6, 60)
        new_user2 = create_account("John", 19, 7, 70)
        all_users = User.objects.all()
        self.assertQuerysetEqual(all_users, ['<User: James>', '<User: John>'], ordered=False)
