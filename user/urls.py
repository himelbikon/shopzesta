from django.urls import path
from .views import *

app_name = 'user'

urlpatterns = [
    path('', index, name='index'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
