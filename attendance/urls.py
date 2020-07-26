from django.urls import path, include
from attendance import views
from django.contrib import admin

app_name = 'attendance'

urlpatterns = [
        path('attendance/', views.attendance, name='list-attendance'),
        # path('check_in_time/', views.check_in_time, name='check_in_time'),
        path('check_out_time/', views.check_out_time, name='check_out_time'),
        path('create_task/', views.create_task, name='create_task'),
        path('delete/task/<int:id>', views.delete_task, name='delete_task'),
        path('update/<slug:slug_text>', views.edit_task, name='edit_task'),
        path('open/all-tasks/<int:id>', views.edit_inline_tasks, name='edit-all-tasks'),
        path('list-tasks/<int:id>', views.list_tasks, name='list-tasks'),
]
