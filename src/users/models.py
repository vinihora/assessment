from django.db import models
from django.db.models.fields.related import ManyToManyField
from .utils import *
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from profiles.models import Answers, Avaliation, Question, Category

# Create your models here.

class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name   = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email= models.EmailField(max_length=200)
    country= models.CharField(max_length=200, blank=True)
    avatar= models.ImageField(default='avatar.png', upload_to='avatars/')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"

    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug=="":
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                ex = Profile.objects.filter(slug = to_slug).exists()
                while (ex):
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Profile.objects.filter(slug = to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)

class Company(models.Model):
    company = models.CharField(max_length=300)
    logo = models.ImageField(default='teste.jpg', upload_to='companies/')

    def __str__(self):
        return self.company

class Teams(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    team = models.CharField(max_length=300)
    user = models.ManyToManyField(Profile, blank=True, related_name='users')
    avaliations = models.ManyToManyField(Avaliation, related_name="avaliations")

    def __str__(self):
        return self.team

class Choice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choiced = models.CharField(max_length=300)
    #choiced = models.CharField(max_length=50, blank=True)
    quest = models.ForeignKey(Question, related_name='quest', on_delete=models.CASCADE, blank=True)
    assess = models.ForeignKey(Avaliation, related_name='assessment', on_delete=models.CASCADE, blank=True)
    #quest = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f"{self.user.username}-{self.quest.id}-{self.assess}"