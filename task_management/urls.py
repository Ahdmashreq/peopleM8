from django.urls import path
from task_management import views

# TEMPLATE TAGGING
app_name = 'task_management'

urlpatterns = [
               path('tasks/list/', views.project_task_list_view, name='task-list'),
               path('tasks/create/', views.project_task_create_view, name='tasks-create'),

]
