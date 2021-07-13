from django.contrib import admin

from profiles.models import Avaliation, Category, Question, Answers

# Register your models here.

admin.site.register(Avaliation)
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Answers)