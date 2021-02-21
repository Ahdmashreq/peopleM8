from django.urls import path, include
from element_definition import views

app_name='element_definition'

urlpatterns=[
    path('command/run/', views.installElementMaster, name= 'command-run'),
    path('element/', include([
                ######################### Element URLs #####################################
                path('new/', views.create_new_element, name='element-create'),
                path('list/', views.list_elements_view, name='list-element'),
                path('update/<int:pk>/', views.update_element_view, name='update-element'),
                path('delete/<int:pk>/', views.delete_element_view, name='delete-element'),
                path('ajax/', views.fast_formula, name=' fast_formula'),

    ])),
    path('batch/', include([
                ######################### ElementBatch URLs ################################
                path('new/', views.create_salary_structure_with_elements_view, name='batch-create'),
                path('list/', views.list_salary_structures, name='list-batchs'),
                path('update/<int:pk>/', views.update_salary_structure_with_elements_view, name='update-batch'),
                path('delete/<int:pk>/', views.delete_salary_structure_with_elements_view, name='delete-batch'),
    ])),
    path('link/', include([
                ######################### ElementLink URLs #################################
                path('new/', views.createElementLinkView, name='link-create'),
                path('list/', views.listElementLinkView, name='list-links'),
                path('update/<int:pk>/', views.updateElementLinkView, name='update-link'),
                path('delete/<int:pk>/', views.deleteElementLinkView, name='delete-link'),

    ])),
    ######################### Custom Rules URLs #################################
    path('custom/rules/new/', views.customRulesView, name='custom-rules-create'),
    path('custom-rules/', views.customRulesView, name='list-custom-rules'),
    path('custom/rules/update/<int:pk>/', views.edit_custom_rule, name='update-custom-rules'),
    path('custom/rules/delete/<int:pk>/', views.delete_custom_rule, name='delete-custom-rules'),

]
