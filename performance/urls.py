from django.urls import path, include
from django.contrib.auth.decorators import login_required
from performance import views

# gehad : createPerformance urls.
app_name= 'performance'

urlpatterns =[
    path('performance/', include([
            ######################### Performance URLs ###################################
            path('create/', views.createPerformance, name='performance-create'),
            path('list/', views.listPerformance, name='performance-list'),
            path('create/rating/<int:per_id>', views.createPerformanceRating, name='rating-create'),
            path('management/', views.performanceManagement, name='management'),

              ])),
]
        