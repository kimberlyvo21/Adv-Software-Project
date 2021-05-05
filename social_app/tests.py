'''
Documentation
This file contains all the testing involved with the web application.
- Sources
- https://docs.djangoproject.com/en/3.2/intro/tutorial05/   -   How to do unit testing in django/python
- https://docs.python.org/3/library/unittest.html   -   Different types of assert statements
'''

from django.test import TestCase
from .models import Profile, Workouts, Dashboard
from django.contrib.auth.models import User
import math


# Create your tests here.

def create_account(username, age, height, level, email):
    User.objects.create_user(username=username, email=email)
    return Profile.objects.create(User=User.objects.get(username=username), name="John Doe", age=age, height=height,
                                  level=level,
                                  email="John@gmail.com")

class ProfileCreation(TestCase):
    def test_case_profile_accept(self):
        new_user = create_account("James", 18, 6, 60, "James@gmail.com")
        all_users = User.objects.all()
        self.assertQuerysetEqual(all_users, ['<User: James>'])

    def test_case_profile_more_than_one(self):
        new_user = create_account("James", 18, 6, 60, "James@gmail.com")
        new_user2 = create_account("John", 19, 7, 70, "John@gmail.com")
        all_users = User.objects.all()
        self.assertQuerysetEqual(all_users, ['<User: James>', '<User: John>'], ordered=False)


class WorkOut(TestCase):
    def test_WorkOutAdded(self):
        new_user = create_account("James", 18, 6, 60, "James@gmail.com")
        new_workout = Workouts(User=User.objects.get(username="James"), Workout_Name=["PushUps"], Workout_Progress=[0],
                               Workout_Goals=[60])
        self.assertQuerysetEqual(new_workout.Workout_Name, ["'PushUps'"], ordered=False)

    def test_WorkOutNotAdded(self):
        can_add = False
        new_user = create_account("James", 18, 6, 60, "James@gmail.com")
        new_workout = Workouts(User=User.objects.get(username="James"), Workout_Name=["PushUps"], Workout_Progress=[0],
                               Workout_Goals=[60])
        try:
            number = new_workout.Workout_Name.index("PushUps")
        except ValueError:
            can_add = True
        self.assertEqual(can_add, False)

    def test_WorkOutProgress(self):
        new_user = create_account("James", 18, 6, 60, "James@gmail.com")
        new_workout = Workouts(User=User.objects.get(username="James"), Workout_Name=["PushUps"], Workout_Progress=[0],
                               Workout_Goals=[60])
        index = new_workout.Workout_Name.index("PushUps")
        new_workout.Workout_Progress[index] += int(20)
        self.assertEqual(new_workout.Workout_Progress[index], 20)

    def test_WorkOutCompletion(self):
        new_user = create_account("James", 18, 6, 60, "James@gmail.com")
        new_workout = Workouts.objects.create(User=User.objects.get(username="James"), Workout_Name=["PushUps"],
                                              Workout_Progress=[0],
                                              Workout_Goals=[60])
        index = new_workout.Workout_Name.index("PushUps")
        new_workout.Workout_Progress[index] += int(70)
        if new_workout.Workout_Progress[index] >= new_workout.Workout_Goals[index]:
            new_workout.Workout_Progress[index] = new_workout.Workout_Goals[index]
        self.assertEqual(new_workout.Workout_Progress[index], 60)


class Friend(TestCase):
    def test_FriendAdded(self):
        userExists = True
        new_user = create_account("James", 18, 6, 60, "James@gmail.com")
        new_user2 = create_account("John", 1, 1, 1, "John@gmail.com")
        Dashboard_User = Dashboard(User=User.objects.get(email="James@gmail.com"), Friends=[], Workout=[])
        try:
            Dashboard_User.Friends.append("John")
        except Profile.DoesNotExist:
            userExists = False
        friends = Dashboard_User.Friends
        self.assertEqual(userExists, True)
        self.assertEquals(friends, ['John'])

    def test_FriendNotFound(self):
        userExists = True
        new_user = create_account("James", 18, 6, 60, "James@gmail.com")
        Dashboard_User = Dashboard(User=User.objects.get(email="James@gmail.com"), Friends=[], Workout=[])
        try:
            Profile.objects.get(email="Bob@gmail.com")
            Dashboard_User.Friends.append("Bob")
        except Profile.DoesNotExist:
            userExists = False
        friends = Dashboard_User.Friends
        self.assertEqual(userExists, False)
        self.assertEqual(friends, [])

    def test_FriendAlready(self):
        userExists = True
        new_user = create_account("James", 18, 6, 60, "James@gmail.com")
        new_user2 = create_account("John", 1, 1, 1, "John@gmail.com")
        Dashboard_User = Dashboard(User=User.objects.get(email="James@gmail.com"), Friends=["John"], Workout=[])
        try:
            #Profile.objects.get(email="John@gmail.com")
            if "John" not in Dashboard_User.Friends:
                Dashboard_User.Friends.append("John")
            else:
                print("John already added")
        except Profile.DoesNotExist:
            userExists = False
        friends = Dashboard_User.Friends
        self.assertEqual(userExists, True)
        self.assertEqual(friends, ["John"])

    def test_FriendSelf(self):
        userExists = True
        new_user = create_account("James", 18, 6, 60, "James@gmail.com")
        Dashboard_User = Dashboard(User=User.objects.get(email="James@gmail.com"), Friends=[], Workout=[])
        try:
            if Dashboard_User.User.username == "James":
                print("You can't add yourself")
            else:
                Dashboard_User.Friends.append("James")
        except Profile.DoesNotExist:
            userExists = False
        friends = Dashboard_User.Friends
        self.assertEqual(userExists, True)
        self.assertEqual(friends, [])
        
        
class Level(TestCase):
    def test_LevelSame(self):
        level_val = 0
        level = 0
        new_user = create_account("James", 18, 6, 60, "James@gmail.com")
        new_workout = Workouts(User=User.objects.get(username="James"), Workout_Name=["PushUps"], Workout_Progress=[0],
                               Workout_Goals=[60])
        index = new_workout.Workout_Name.index("PushUps")
        new_workout.Workout_Progress[index] += int(20)
        for num in new_workout.Workout_Progress:
            level_val = (num + level_val)
        level = math.floor(level_val / 100)
        self.assertEqual(level, 0)

    def test_LevelNext(self):
        level_val = 0
        level = 0
        new_user = create_account("James", 18, 6, 60, "James@gmail.com")
        new_workout = Workouts(User=User.objects.get(username="James"), Workout_Name=["PushUps"], Workout_Progress=[0],
                               Workout_Goals=[100])
        index = new_workout.Workout_Name.index("PushUps")
        new_workout.Workout_Progress[index] += int(100)
        for num in new_workout.Workout_Progress:
            level_val = (num + level_val)
        level = math.floor(level_val / 100)
        self.assertEqual(level, 1)
        
        
class Leaderboard(TestCase):
    def test_LevelSame(self):
        level_val = 0
        level_val1 = 0
        level = 0
        level1 = 0
        james_first = False
        new_user = create_account("James", 18, 6, 60, "James@gmail.com")
        new_workout = Workouts(User=User.objects.get(username="James"), Workout_Name=["PushUps"], Workout_Progress=[0],
                               Workout_Goals=[100])
        index = new_workout.Workout_Name.index("PushUps")
        new_workout.Workout_Progress[index] += int(100)
        for num in new_workout.Workout_Progress:
            level_val = (num + level_val)
        level = math.floor(level_val / 100)
        self.assertEqual(level, 1)
        # -----
        new_user1 = create_account("John", 18, 6, 60, "John@gmail.com")
        new_workout1 = Workouts(User=User.objects.get(username="John"), Workout_Name=["PushUps"], Workout_Progress=[0],
                               Workout_Goals=[100])
        index1 = new_workout.Workout_Name.index("PushUps")
        new_workout1.Workout_Progress[index1] += int(100)
        for num in new_workout1.Workout_Progress:
            level_val1 = (num + level_val1)
        level1 = math.floor(level_val1 / 100)
        self.assertEqual(level1, 1)
        # -----
        list_levels = [level, level1]
        list_levels.sort(reverse=True)
        self.assertEqual(list_levels, [1, 1])

    def test_LevelDifferent(self):
        level_val = 0
        level_val1 = 0
        level = 0
        level1 = 0
        james_first = False
        new_user = create_account("James", 18, 6, 60, "James@gmail.com")
        new_workout = Workouts(User=User.objects.get(username="James"), Workout_Name=["PushUps"],
                               Workout_Progress=[0],
                               Workout_Goals=[200])
        index = new_workout.Workout_Name.index("PushUps")
        new_workout.Workout_Progress[index] += int(200)
        for num in new_workout.Workout_Progress:
            level_val = (num + level_val)
        level = math.floor(level_val / 100)
        self.assertEqual(level, 2)
        # -----
        new_user1 = create_account("John", 18, 6, 60, "John@gmail.com")
        new_workout1 = Workouts(User=User.objects.get(username="John"), Workout_Name=["PushUps"],
                                Workout_Progress=[0],
                                Workout_Goals=[100])
        index1 = new_workout.Workout_Name.index("PushUps")
        new_workout1.Workout_Progress[index1] += int(100)
        for num in new_workout1.Workout_Progress:
            level_val1 = (num + level_val1)
        level1 = math.floor(level_val1 / 100)
        self.assertEqual(level1, 1)
        # -----
        list_levels = [level1, level]
        list_levels.sort(reverse=True)
        self.assertEqual(list_levels, [2, 1]) 
