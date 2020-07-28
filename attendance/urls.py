from attendance import views
from django.urls import path

app_name = 'attendance'

urlpatterns = [
        path('attendance/', views.list_attendance, name='list-attendance'),
        path('check_out_time/', views.check_out_time, name='check_out_time'),
        path('create_task/', views.create_task, name='create_task'),
        path('delete/task/<slug:text_slug>', views.delete_task, name='delete_task'),
        path('update/<slug:slug_text>', views.edit_task, name='edit_task'),
        path('open/all-tasks/<int:id>', views.edit_inline_tasks, name='edit-all-tasks'),
        path('list-tasks/<slug:slug_text>', views.list_tasks_view, name='list-tasks'),
]
