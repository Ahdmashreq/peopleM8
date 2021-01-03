from django.urls import path

from company.api import views

app_name = 'api-inventory'

urlpatterns = [
    path('departments/', views.DepartmentListView.as_view(), name='list-uom-categories'),
    ]