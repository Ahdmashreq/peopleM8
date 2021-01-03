from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from company.api.serializers import DepartmentSerializer
import random

from company.models import Department


class DepartmentListView(ListAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_fields = ('id',)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Department.objects.filter(end_date__isnull=True)

