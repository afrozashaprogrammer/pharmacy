from django.urls import path
from .views import *
app_name = 'administration' 
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('billing/', billing, name='billing'),
    path('users/', users, name='users'),
    path('new-user/', new_user, name='new_user'),
    path('edit-user/<int:id>/', edit_user, name='edit_user'),
    path("tests/", tests, name="tests"),
    path("tests-create/", create_test, name="create_test"),
    path("tests-update/<int:test_id>/",update_test, name="update_test"),
    
]