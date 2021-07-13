from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from profiles.models import *
from profiles.models import *
from django.contrib.auth.models import User


# Create your views here.


def test_view(request):
    profile = Profile.objects.get(user = request.user)
    questions = Question.objects.filter(category__name='Coachable')

    context = {
        'profile':profile,
        'questions':questions,
    }

    return render(request, 'users/home.html', context)


def dashboard(request):
    profile = Profile.objects.get(user = request.user)
    