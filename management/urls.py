from django.urls import path
from .views import *
app_name = 'management' 
urlpatterns = [
    path('', dashboard, name='dashboard'),
]