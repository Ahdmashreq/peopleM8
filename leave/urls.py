from django.urls import path
from leave import views

app_name = 'leave'

urlpatterns = [
    path('list_leave/', views.list_leave, name='list_leave'),
    path('del_leave/<int:id>', views.delete_leave_view, name='del_leave'),
    path('add_leave/', views.add_leave, name='add_leave'),
    path('edit_leave/<int:id>', views.edit_leave, name='edit_leave'),
    path('add_leave_master/', views.add_leave_master, name='add_leave_master'),
    path('list-leave-master/', views.list_leave_master, name='list-leave-master'),
    path('edit_leave_master/<int:id>', views.edit_leave_master, name='edit_leave_master'),
    path('del_leave_master/<int:id>', views.del_leave_master, name='del_leave_master'),
    path('leave-approve/<int:leave_id>/<str:redirect_to>/', views.leave_approve, name='leave-approve'),
    path('leave-unapprove/<int:leave_id>/<str:redirect_to>/', views.leave_unapprove, name='leave-unapprove'),
    path('leave-balance/', views.Elmplyees_Leave_Balance.as_view(), name='leave-balance'),

    path('leave-balance/edit/<int:leave_balance_id>/', views.edit_employee_leaves_balance, name='leave_balance_edit'),
    path('leave-balance/delete/<int:leave_balance_id>/', views.delete_leave_balance, name='leave_balance_delete'),

    path('leave-balance-add/', views.create_employee_leave_balance, name='leave-balance-create'),
    path('leave-balance-list/<int:employee_id>/', views.view_employee_leaves_list, name='employee-leave-list'),
    path('amira/', views.get_leave_type, name='leave_type'),

]
