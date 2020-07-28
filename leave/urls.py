from django.urls import path
from leave import views
from django.contrib import admin

app_name = 'leave'

urlpatterns = [
    path('list_leave/', views.list_leave, name='list_leave'),
    path('del_leave/<int:id>', views.delete_leave_view, name='del_leave'),
    path('add_leave/', views.add_leave, name='add_leave'),
    path('edit_leave/<int:id>', views.edit_leave, name='edit_leave'),
    path('add_leave_master/', views.add_leave_master, name='add_leave_master'),
    path('edit_leave_master/<int:id>', views.edit_leave_master, name='edit_leave_master'),
    path('del_leave_master/<int:id>', views.del_leave_master, name='del_leave_master'),
    path('leave-approve/<int:leave_id>', views.leave_approve, name='leave-approve'),
    path('leave-unapprove/<int:leave_id>', views.leave_unapprove, name='leave-unapprove'),
]
