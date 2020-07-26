from django.urls import path, include
from defenition import views


app_name= 'defenition'

urlpatterns=[
             path('lookups/', include([
                ######################### Lookup URLs ###################################
                path('new/', views.createLookupView, name='lookup-create'),
                path('list/', views.listLookupView, name='list-lookups'),
                path('update/<int:pk>/', views.updateLookupView, name='update-lookup'),
                path('delete/<int:pk>/', views.deleteLookupView, name='delete-lookup'),
             ])),
             path('rules/', include([
                path('insurance/', include([
                      ######################### Insurance URLs ###################################
                      path('list/', views.list_insurance_rules, name= 'insurance-list'),
                      path('create/', views.create_insurance_rules, name= 'insurance-create'),
                      path('update/<int:pk>', views.update_insurance_rule, name= 'insurance-update'),
                      path('delete/<int:pk>', views.delete_insurance_rule, name= 'insurance-delete'),
                      path('egy/insurance/rule/', views.copy_insurance_rule, name= 'egypt-insuracne-rule'),
                ])),
                path('tax/', include([
                     ######################### Tax URLs ###################################
                     path('list/', views.list_tax_rules, name= 'tax-list'),
                     path('create/', views.create_tax_rules, name= 'tax-create'),
                     path('update/<int:pk>', views.update_tax_rule, name= 'tax-update'),
                     path('delete/<int:pk>', views.delete_tax_rule, name= 'tax-delete'),
                     path('egy/tax/rule/', views.copy_tax_rule, name= 'egypt-tax-rule'),
                ])),
             ])),

            path('command/run/', views.runningManagementCommand, name= 'command-run'),
]
