from django.urls import path
from .views import *
app_name = 'management' 
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('counter/', counter_dashboard, name="counter_dashboard"),
    path('counter/patient-test/', patient_test, name='patient_test'),
    path("counter/patient-search/", patient_search, name="patient_search"),
    path("counter/patient/<int:pk>/select/", patient_select, name="patient_select"),
    path("counter/patient/create-form/", patient_create_form, name="patient_create_form"),
]