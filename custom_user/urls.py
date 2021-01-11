from django.urls import path
from .views import *
urlpatterns=[
    path('groups/new',create_groups),
   
]