from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
        path('i18n/', include('django.conf.urls.i18n')),
        path('arkleab4superadmin/', admin.site.urls),
        path( '', include('home.urls'), name='home'),
        path('currencies/', include('currencies.urls')),
        path('com/', include('company.urls')),
        path('emp/', include('employee.urls')),
        path('defenition/', include('defenition.urls')),
        path('manage/', include('manage_payroll.urls')),
        path('payroll/', include('payroll_run.urls')),
        path('element/', include('element_definition.urls')),
        path('costing/', include('balanc_definition.urls')),
        path('leave/', include('leave.urls')),
        path('notification/', include('notification.urls')),
        path('attendance/', include('attendance.urls')),
        path('report/', include('report.urls')),
        path('recruitment/', include('recruitment.urls')),
        path('service/', include('service.urls')),
        path('api/company/', include('company.api.urls')),

              ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# urlpatterns += i18n_patterns (
#
# )
