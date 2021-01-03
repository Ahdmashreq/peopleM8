from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from account.models import Customer, Supplier
from inventory.api.serializers import UomCategorySerializer, UomSerializer, CategorySerializer, BrandSerializer, \
    AttributeSerializer, StokeTakeSerializer, StokeEntrySerializer
from rest_framework.permissions import IsAuthenticated
import random

from inventory.models import UomCategory, Uom, Category, Brand, Attribute, StokeTake, StokeEntry, Product, Item
from inventory.views import create_stoke_transaction
from orders.models import Inventory_Balance


class DepartmentListView(ListAPIView):
    serializer_class = UomCategorySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_fields = ('id', 'slug',)
    ordering_fields = ('name',)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        company = self.request.user.company
        return UomCategory.objects.filter(company=company)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            data = {"success": True, "data": serializer.data, "count": paginated_response.data["count"]}
            return Response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = {"success": True, "data": serializer.data}
        return Response(data)

