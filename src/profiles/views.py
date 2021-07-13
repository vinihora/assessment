from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from users.models import *
from profiles.models import *
from django.contrib.auth.models import User

# Create your views here.
def myprofile_view(request):
    profile = Profile.objects.get(user = request.user)
    teams = Teams.objects.filter(user = profile)
    company = Company.objects.get()
    context = {
        'profile':profile,
        'teams':teams
    }

    return render(request, 'profiles/myprofile.html', context)
