from django.urls import path, include
from django.contrib.auth.decorators import login_required
from performance import views

app_name= 'performance'

urlpatterns =[
    path('performance/', include([
            ######################### Performance URLs ###################################
            path('create/', views.createPerformance, name='performance-create'),
              ])),

]
        