from django.core.exceptions import PermissionDenied
from company.models import Enterprise
from custom_user.models import User


def user_is_author(function):
    def wrap(request, *args, **kwargs):
        users_company = User.objects.filter(company = request.user.company)
        logged_user = Enterprise.objects.get(created_by__in=users_company)
        if logged_user == request.user.company:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def list_data_by_company(self, request):
    users_company = User.objects.filter(company = request.user.company)
    return self.objects.filter(created_by__in=users_company)

def any_company_data(self, request):
    users_company = User.objects.filter(company = request.user.company)
    return self.objects.filter(global_flag=True)
