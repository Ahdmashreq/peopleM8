from django.urls import path, include
from django.contrib.auth.decorators import login_required
from employee import views
from urllib.parse import quote
from django.utils.encoding import iri_to_uri, uri_to_iri

app_name= 'employee'

urlpatterns =[
    path('employee/', include([
            ######################### Employee URLs ###################################
            path('new/', views.createEmployeeView, name='employee-create'),
            path('element/', views.copy_element_values, name='element-create'),
            path('information/listT/', views.listEmployeeView , name='list-employee'),
            path('information/listC/', views.listEmployeeCardView , name='list-employee-card'),
            path('correct/<int:pk>/', views.correctEmployeeView, name='correct-employee'),
             path('update/<int:pk>/', views.updateEmployeeView, name='update-employee'),
            path('view/<int:pk>/', views.viewEmployeeView, name='view-employee'),
            path('delete/<int:pk>/', views.deleteEmployeeView, name='delete-employee'),
            path('delete/forever/<int:pk>/', views.deleteEmployeePermanently, name='delete-employee-permanently'),

            path('link/employee/<int:pk>/structure/', views.create_link_employee_structure, name='link-structure-create'),
            path('update/link/employee/<int:pk>/structure/', views.update_link_employee_structure, name='link-structure-update'),
            path('ajax/', views.change_element_value, name='change-element-value'),
            path('employee/export/', views.export_employee_data, name='employee-export'),
            path('jobroll/new/<int:job_id>', views.createJobROll, name='new-jobroll'),
            path('leaves-history/' , views.list_employee_leave_requests , name='leaves-history'),
            path('element/new/<int:job_id>', views.create_employee_element, name='new-employee-element'),





    ])),

]
