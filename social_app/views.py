from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Profile
from django.contrib.auth.models import User



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
            profile_idea = Profile(User = User.objects.get(email=email) ,name=name_p, age=age_p, height=height_p, time=time_p, email=email)
            profile_idea.save()
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
