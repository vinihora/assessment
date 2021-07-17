from django.urls import path
from .views import *

app_name = 'profiles'

urlpatterns = [
    path('myprofile/', myprofile_view, name='myprofile-view'),
    path('assessment/<int:assessment>/', assessment_view, name='assessment-view'),
    path('assessment/results/', assessment_results_view, name='assessment-results-view'),
    path('myprofile/results/', results, name='results-view'),
]