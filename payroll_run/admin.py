from django.contrib import admin
from payroll_run. models import Salary_elements

@admin.register(Salary_elements)
class SalaryElementsAdmin(admin.ModelAdmin):
    model = Salary_elements
    list_display = ('emp','salary_month', 'salary_year',)
