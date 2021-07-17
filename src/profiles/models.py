from typing import Text
from django.db import models
from django.shortcuts import reverse

# Create your models here.

class Answers(models.Model):
    
    ans = models.CharField(max_length=200)
    def __str__(self):
        return self.ans

class Question(models.Model):
    question = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

class Category(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    questions = models.ManyToManyField(Question, related_name='questions')
    choices = models.ManyToManyField(Answers, related_name="choices")

    def __str__(self):
        return self.name

# Tipo do assess: perfil intraempreendedor, modelos ágeis, inovação 1 ou inovação 2.

TYPE_CHOICE = (
    ('pontuação','pontuação'),
    ('representação','representação')
)

class Avaliation(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, related_name='category')
    value = models.CharField(choices = TYPE_CHOICE, max_length=20, default='pontuação', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("profiles:assessment-view", kwargs={"assessment": self.id})