from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Profile


def Signup(request):
    name_p = ""
    age_p = ""
    height_p = ""
    time_p = ""
    email_p = ""
    print(request.method)
    if request.method == 'GET':
        return render(request, 'social_app/signup.html')
    if request.method == 'POST':
        name_p = request.POST.get('name')
        age_p = request.POST.get('age')
        height_p = request.POST.get('height')
        time_p = request.POST.get('time')
        email_p = request.POST.get('email')
    profile_idea = Profile(name=name_p, age=age_p, height=height_p, time=time_p, email=email_p)
    if(name_p and age_p and time_p):
        profile_idea.save()
        return render(request, 'social_app/signup.html')
    else:
        return HttpResponseRedirect(reverse('social_url:signup'))
        
