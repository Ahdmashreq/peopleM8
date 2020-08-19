from attendance import views
from django.urls import path

app_name = 'attendance'

urlpatterns = [
        path('attendance/', views.list_attendance, name='user-list-attendance'),
        path('check_out_time/', views.check_out_time, name='check_out_time'),
        path('create_task/', views.create_task, name='create_task'),
        path('delete/task/<slug:slug_text>/', views.delete_task, name='delete_task'),
        path('update/<slug:slug_text>/', views.edit_task_view, name='edit-task'),
        path('open/all-tasks/<slug:attendance_text>/', views.edit_inline_tasks, name='edit-all-tasks'),
        path('list-tasks/<slug:attendance_slug>/', views.list_tasks_view, name='list-tasks'),
        path('upload-file/', views.upload_xls_file, name='upload-attendance'),
        path('confirm-file/', views.confirm_xls_upload, name='confirm-upload'),
        path('list-attendance/', views.list_all_attendance, name='emp-attendance'),
        path('update-attendance/<slug:att_update_slug>/', views.update_attendance, name='update-attendance'),
        path('delete-attendance/<slug:att_delete_slug>/', views.delete_attendance, name='delete-attendance'),

]
