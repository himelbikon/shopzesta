from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    # path('about_us', about_us, name='about_us'),
    path('terms_and_conditions', terms_and_conditions,
         name='terms_and_conditions'),
]
