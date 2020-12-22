from django.urls import path
from service import views




# TEMPLATE TAGGING
app_name= 'service'
urlpatterns = [
                   path('bussiness/travel/list/', views.services_list, name='services_list'),
                   path('bussiness/travel/delete/<int:id>', views.services_delete, name='services_delete'),
                   path('bussiness/travel/edit/<int:id>', views.services_edit, name='services_edit'),
                   path('bussiness/travel/update/<int:id>/', views.services_update, name='services-update'),
                   path('services/create/', views.services_create, name='services_create'),
                   path('service/approve/<int:service_id>', views.service_approve, name='service-approve'),
                   path('service/unapprove/<int:service_id>', views.service_unapprove, name='service-unapprove'),

                   path('purchase/list/', views.purchase_request_list, name='purchase-request-list'),
                   path('purchase/order/create/', views.purchase_request_create, name='purchase-request-create'),
                   path('purchase/order/update/<int:id>/', views.purchase_request_update, name='purchase-request-update'),
                   path('purchase/approve/<int:order_id>', views.purchase_request_approve, name='purchase-approve'),
                   path('purchase/unapprove/<int:order_id>', views.purchase_request_unapprove, name='purchase-unapprove'),
   ]
