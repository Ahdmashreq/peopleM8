from django.urls import path
from notification import views
from django.contrib import admin



# TEMPLATE TAGGING
app_name= 'notification'
urlpatterns = [
               path('list_notification/', views.list_notification, name='list_notification'),
               path('clear_all/', views.clear_all, name='clear_all'),
               path('change_status/<int:id>', views.change_status, name='change_status'),
               ]
