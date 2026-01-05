from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', login, name='login'),
    path('', home, name='home'),
    path('logout/', logout, name='logout'),
]