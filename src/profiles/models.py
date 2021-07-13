from typing import Text
from django.db import models

# Create your models here.

class Answers(models.Model):
    
    ans = models.CharField(max_length=200)
    def __str__(self):
        return self.ans

class Question(models.Model):
    question = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    answers = models.ManyToManyField(Answers, related_name='answers')

    def __str__(self):
        return self.question

class Category(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    questions = models.ManyToManyField(Question, related_name='questions')

    def __str__(self):
        return self.name

# Tipo do assess: perfil intraempreendedor, modelos ágeis, inovação 1 ou inovação 2.
class Avaliation(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, related_name='category')

    def __str__(self):
        return self.name