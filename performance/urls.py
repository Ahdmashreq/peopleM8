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
            path('create/rating/<int:per_id>/', views.createPerformanceRating, name='rating-create'),
            path('management/', views.performanceManagement, name='management'),
            path('list/perf_rating/<int:ret_id>/', views.listRatingPerformance, name='performance-rating-list'),
            path('create/segment/<int:per_id>/<int:ret_id>/', views.createSegment, name='segment-create'),
            path('list/segment/<int:ret_id>/', views.listSegmentperType, name='segment-list'),

              ])),
]
        