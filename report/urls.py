from django.urls import path, include
from report import views
from django.contrib import admin



# TEMPLATE TAGGING
app_name= 'report'
urlpatterns = [
               path('all_reports/', views.all_reports, name='all_reports'),
               path('late_report/', views.late_report, name='late_report'),
               path('all_people_report/', views.all_people_report, name='all_people_report'),
               ]
