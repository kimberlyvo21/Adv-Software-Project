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



def ProfilePage(request, email):
    try:
        User.objects.get(email=email)
        selected_profile = Profile.objects.get(email=email)
    except(KeyError, User.DoesNotExist, Profile.DoesNotExist):
        name_p = ""
        age_p = ""
        height_p = ""
        time_p = ""
        if request.method == 'GET':
            return render(request, 'social_app/signup.html')
        if request.method == 'POST':
            name_p = request.POST.get('name').lower()
            age_p = request.POST.get('age')
            height_p = request.POST.get('height')
            time_p = request.POST.get('time')
            profile_idea = Profile(User = User.objects.get(email=email), name=name_p, age=age_p, height=height_p, time=time_p, email=email)
            Dashboard_User = Dashboard(User = User.objects.get(email=email), Friends=[], Workout=[])
            Workouts_User = Workouts(User = User.objects.get(email=email), Workout_Name=[], Workout_Progress=[], Workout_Goals=[])
            profile_idea.save()
            Dashboard_User.save()
            Workouts_User.save()
            return render(request, "social_app/profile.html", {
                'name': name_p,
                'age': age_p,
                'height' : height_p,
                'time' : time_p,
            })
    return render(request, "social_app/profile.html", {
                    'name': selected_profile.name,
                    'age': selected_profile.age,
                    'height' : selected_profile.height,
                    'time' : selected_profile.time,
                })

def DashboardPage(request, email):
    Dashboard_User = Dashboard.objects.get(User = User.objects.get(email=email))
    selected_profile = Profile.objects.get(email=email)
    Workouts_User = Workouts.objects.get(User = User.objects.get(email=email))
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

def WorkoutPage(request, email):
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
        }

        video_ids = []
        r = requests.get(search_url, params=search_params)
        results = r.json()['items']

        for result in results:
            print(result)
            video_ids.append(result['id']['videoId'])

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

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

def FriendPage(request, email, name):
    friend_profile = Profile.objects.get(name=name)
    return render(request, "social_app/FriendPage.html", {
            'name_f' : friend_profile.name,
            'time_f' : friend_profile.time,
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