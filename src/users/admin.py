from django.contrib import admin
from .models import Profile, Choice, Teams, Company
# Register your models here.

admin.site.register(Profile)
admin.site.register(Choice)
admin.site.register(Teams)
admin.site.register(Company)
