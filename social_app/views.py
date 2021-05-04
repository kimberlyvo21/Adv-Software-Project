from mysite.settings import YOUTUBE_DATA_API_KEY
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from .models import Profile, Workouts, Dashboard
from django.contrib.auth.models import User
import requests
from isodate import parse_duration
from django.conf import settings
import math



def ProfilePage(request, email):
    try:
        User.objects.get(email=email)
        selected_profile = Profile.objects.get(email=email)
    except(KeyError, User.DoesNotExist, Profile.DoesNotExist):
        name_p = ""
        age_p = ""
        height_p = 0.0
        heightft_p = 0
        heightin_p = 0
        if request.method == 'GET':
            return render(request, 'social_app/signup.html')
        if request.method == 'POST':
            name_p = request.POST.get('name').lower()
            age_p = request.POST.get('age')
            heightft_p = request.POST.get('heightfeet')
            heightin_p = request.POST.get('heightinches')
            if (int(heightin_p) > 9):
                height_p = float(int(heightft_p) + (int(heightin_p)/100))
            else:
                height_p = float(int(heightft_p) + (int(heightin_p)/10))
            try:
                Profile.objects.get(name=name_p)
            except(Profile.DoesNotExist):
                profile_idea = Profile(User = User.objects.get(email=email), name=name_p, age=age_p, height=height_p, level=0, email=email)
                Dashboard_User = Dashboard(User = User.objects.get(email=email), Friends=[], Workout=[])
                Workouts_User = Workouts(User = User.objects.get(email=email), Workout_Name=[], Workout_Progress=[], Workout_Goals=[])
                profile_idea.save()
                Dashboard_User.save()
                Workouts_User.save()
                return render(request, "social_app/profile.html", {
                    'name': name_p,
                    'age': age_p,
                    'height' : height_p,
                    'level' : 0,
                })
            return render(request, 'social_app/signup.html', {
                'error' : "The username is taken"
            })
    return render(request, "social_app/profile.html", {
                    'name': selected_profile.name,
                    'age': selected_profile.age,
                    'height' : selected_profile.height,
                    'level' : selected_profile.level,
                })

def DashboardPage(request, email):
    Dashboard_User = Dashboard.objects.get(User = User.objects.get(email=email))
    selected_profile = Profile.objects.get(email=email)
    Workouts_User = Workouts.objects.get(User = User.objects.get(email=email))
    Progress_Num = []
    Name_Prog = []
    for Prog, Goals in zip(Workouts_User.Workout_Progress, Workouts_User.Workout_Goals): {
        Progress_Num.append((Prog/Goals)*100)
    }
    for Prog, Name in zip(Workouts_User.Workout_Progress, Workouts_User.Workout_Name): 
        Name_Prog.append([Name, Prog])
    return render(request, "social_app/Dashboard.html", {
        'name' : selected_profile.name,
        'Friends' : Dashboard_User.Friends,
        'Workouts': Dashboard_User.Workout,
        'Progress' : Progress_Num,
        'length' : len(Dashboard_User.Workout),
        'NameOfProg' : Name_Prog
    })

def WorkoutPage(request, email):
    #Try to see if you can watch the youtube video in browser
    Workouts_User = Workouts.objects.get(User = User.objects.get(email=email))
    Dashboard_User = Dashboard.objects.get(User = User.objects.get(email=email))
    selected_profile = Profile.objects.get(email=email)
    videos = []
    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        search_params = {
            'part' :'snippet',
            'q' : request.POST['search'],
            'key' :  settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 3,
            'type' : 'video'
        }

        video_ids = []
        r = requests.get(search_url, params=search_params)
        results = r.json()['items']

        for result in results:
            video_ids.append(result['id']['videoId'])


        video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 3
        }

        r = requests.get(video_url, params=video_params)
        results = r.json()['items']
        for result in results:
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail' : result['snippet']['thumbnails']['high']['url']
            }

            videos.append(video_data)
    Progress_Num = []
    for Prog, Goals in zip(Workouts_User.Workout_Progress, Workouts_User.Workout_Goals): {
        Progress_Num.append((Prog/Goals)*100)
    }
    context = {
        'videos' : videos,
        'name' : selected_profile.name,
        'Friends' : Dashboard_User.Friends,
        'Workouts': Dashboard_User.Workout,
        'Progress' : Progress_Num,
        'length' : len(Dashboard_User.Workout),
    }
    
    return render(request, 'social_app/WorkoutPage.html', context)
    

def AddFriends(request, email):
    Dashboard_User = Dashboard.objects.get(User = User.objects.get(email=email))
    selected_profile = Profile.objects.get(email=email)
    Workouts_User = Workouts.objects.get(User = User.objects.get(email=email))
    name_p = ""
    if request.method == 'GET':
        return render(request, "social_app/AddFriend.html")
    if request.method == 'POST':  
        name_p = request.POST.get("username").lower()
        try:
            Profile.objects.get(name=name_p)
        except(Profile.DoesNotExist):
            return render(request, "social_app/AddFriend.html", {
                'error' : "Sorry the user was not found"
            })
        if name_p in Dashboard_User.Friends:
            return render(request, "social_app/AddFriend.html", {
                'error': "User is already added"
            })
        elif name_p == selected_profile.name:
            return render(request, "social_app/AddFriend.html", {
                'error': "User you are trying to add is yourself"
            })
        Dashboard_User.Friends.append(name_p)
        Dashboard_User.save()
        Progress_Num = []
        for Prog, Goals in zip(Workouts_User.Workout_Progress, Workouts_User.Workout_Goals): {
            Progress_Num.append((Prog/Goals)*100)
        }
        return render(request, "social_app/Dashboard.html", {
            'name' : selected_profile.name,
            'Friends' : Dashboard_User.Friends,
            'Workouts': Dashboard_User.Workout,
            'Progress' : Progress_Num,
            'length' : len(Dashboard_User.Workout),
        })

def FriendPage(request, email):
    Dashboard_User = Dashboard.objects.get(User = User.objects.get(email=email))
    friends_level = []
    friends_likes = []
    friends = []
    if request.method == 'POST':
        if 'like' in request.POST:
            if request.POST['like'] == 'click':
                selected_profile = Profile.objects.get(name = request.POST.get('name'))
                selected_profile.ThumbsUp += 1
                selected_profile.save()
    for friend in Dashboard_User.Friends: 
        selected_profile = Profile.objects.get(name = friend)
        friends_level.append(selected_profile.level)
        friends_level.sort(reverse=True)
        friends.insert(friends_level.index(selected_profile.level), friend)
        friends_likes.insert(friends_level.index(selected_profile.level), selected_profile.ThumbsUp)

    return render(request, "social_app/FriendPage.html", {
            'name_f' : friends,
            'level_f' : friends_level,
            'likes_f' : friends_likes,
            })

def AddWorkout(request, email):
    Workouts_User = Workouts.objects.get(User = User.objects.get(email=email))
    Dashboard_User = Dashboard.objects.get(User = User.objects.get(email=email))
    selected_profile = Profile.objects.get(email=email)
    name_w = ""
    goals_w = 0
    if request.method == 'GET':
        return render(request, "social_app/AddWorkout.html")
    if request.method == 'POST':  
        name_w = request.POST.get("workoutname")
        goals_w = request.POST.get("workoutgoals")
        try:
            Dashboard_User.Workout.index(name_w)
            Workouts_User.Workout_Name.index(name_w)
        except(ValueError):
            Dashboard_User.Workout.append(name_w)
            Workouts_User.Workout_Name.append(name_w)
            Workouts_User.Workout_Progress.append(0)
            Workouts_User.Workout_Goals.append(int(goals_w))
            Dashboard_User.save()
            Workouts_User.save()
            Progress_Num = []
            for Prog, Goals in zip(Workouts_User.Workout_Progress, Workouts_User.Workout_Goals): {
                Progress_Num.append((Prog/Goals)*100)
            }
            return render(request, "social_app/Dashboard.html", {
                'name' : selected_profile.name,
                'Friends' : Dashboard_User.Friends,
                'Workouts': Dashboard_User.Workout,
                'Progress' : Progress_Num,
                'length' : len(Dashboard_User.Workout),
            })
        return render(request, "social_app/AddWorkout.html", {
            'error' : "Sorry that workout was already created please make a new one",
        })

def UpdateWorkout(request, email):
    Workouts_User = Workouts.objects.get(User = User.objects.get(email=email))
    Dashboard_User = Dashboard.objects.get(User = User.objects.get(email=email))
    selected_profile = Profile.objects.get(email=email)
    name_w = ""
    progress_w = 0
    level_val = 0
    if request.method == 'GET':
        return render(request, "social_app/UpdateWorkout.html")
    if request.method == 'POST':
        name_w = request.POST.get("workoutname")
        progress_w = request.POST.get("workoutprogress")
    try:
        index = Workouts_User.Workout_Name.index(name_w)
    except(ValueError):
        return render(request, "social_app/UpdateWorkout.html", {
            'error' : "Sorry there is no such workout",
        })
    print(progress_w)
    Workouts_User.Workout_Progress[index] += int(progress_w)
    if Workouts_User.Workout_Progress[index] >= Workouts_User.Workout_Goals[index]:
        Workouts_User.Workout_Progress[index] = Workouts_User.Workout_Goals[index]
    Workouts_User.save()
    for num in Workouts_User.Workout_Progress:
        level_val = (num + level_val)

    selected_profile.level = math.floor(level_val/100)
    selected_profile.save()

    Progress_Num = []
    for Prog, Goals in zip(Workouts_User.Workout_Progress, Workouts_User.Workout_Goals): {
        Progress_Num.append((Prog/Goals)*100)
    }
    return render(request, "social_app/Dashboard.html", {
        'name' : selected_profile.name,
        'Friends' : Dashboard_User.Friends,
        'Workouts': Dashboard_User.Workout,
        'Progress' : Progress_Num,
        'length' : len(Dashboard_User.Workout),
    })
