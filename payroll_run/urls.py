from django.urls import path, include
from payroll_run import views

app_name ='payroll_run'
urlpatterns=[
    path('salary/', include([
        path('list/', views.listSalaryView, name='list-salary'),
        path('month/list/<int:month>/<int:year>/', views.listSalaryFromMonth, name='list-month-salary'),
        path('finalize/<int:month>/<int:year>/', views.changeSalaryToFinal, name='finalize-salary'),
        path('delete/<int:month>/<int:year>/', views.delete_salary_view, name='delete-salary'),
        path('month/emp/<int:month_number>/<int:salary_year>/<int:salary_id>/<int:emp_id>/', views.userSalaryInformation, name='emp-payslip'),
        path('create/', views.createSalaryView, name='create-salary'),
        path('payslip/create/<int:month>/<int:year>/<int:salary_id>/<int:emp_id>/', views.render_emp_payslip, name='genereate-salary'),
        path('payslip/create/<int:month>/<int:year>/', views.render_all_payslip, name='all-emp-payslip'),
    ])),
]
