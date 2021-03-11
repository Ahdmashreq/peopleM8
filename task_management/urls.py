from django.urls import path
from task_management import views

# TEMPLATE TAGGING
app_name = 'task_management'

urlpatterns = [
               path('tasks/list/', views.project_task_list_view, name='task-list'),
               path('tasks/create/', views.project_task_create_view, name='tasks-create'),
               path('tasks/update/<int:task_id>/', views.project_task_update_view, name='task-update'),
               path('project/create/', views.project_create_view, name='project-create')

]
