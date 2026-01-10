from django.urls import path
from .views import *
app_name = 'management' 
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('counter/', counter_dashboard, name="counter_dashboard"),
    path('counter/patient-test/', patient_test, name='patient_test'), 
]