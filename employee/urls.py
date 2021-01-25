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
            path('update/<int:pk>/', views.updateEmployeeView, name='update-employee'),
            path('view/<int:pk>/', views.viewEmployeeView, name='view-employee'),
            path('delete/<int:pk>/', views.deleteEmployeeView, name='delete-employee'),

            path('link/employee/<int:pk>/structure/', views.create_link_employee_structure, name='link-structure-create'),
            path('update/link/employee/<int:pk>/structure/', views.update_link_employee_structure, name='link-structure-update'),
            path('ajax/', views.change_element_value, name='change-element-value'),


    ])),

]
