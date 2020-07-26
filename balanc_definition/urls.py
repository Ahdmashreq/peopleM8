from django.urls import path
from urllib.parse import quote
from django.utils.encoding import iri_to_uri
from balanc_definition import views

app_name = 'balanc_definition'

urlpatterns = [
              path(quote('accounts/list/'), views.costAccountList, name= 'list-costing'),
              path(iri_to_uri("account/screate/"), views.costAccountCreate, name= 'create-costing'),
              path('accounts/update/<int:pk>', views.costAccountupdate, name= 'update-costing'),
              path('accounts/delete/<int:pk>', views.costAccountdelete, name= 'delete-costing'),
]
