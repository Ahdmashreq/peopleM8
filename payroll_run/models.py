from django.conf import settings
from django.db import models
from datetime import date
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from employee.models import Employee, JobRoll, Employee_Element, Employee_Element_History
from element_definition.models import Element_Batch
from manage_payroll.models import Assignment_Batch, Payroll_Master
from payroll_run.new_tax_rules import Tax_Deduction_Amount
from django.utils.translation import ugettext_lazy as _

month_name_choises = [
    (1, _('January')), (2, _('February')), (3, _('March')), (4, _('April')),
    (5, _('May')), (6, _('June')), (7, _('July')), (8, _('August')),
    (9, _('September')), (10, _('October')
                          ), (11, _('November')), (12, _('December')),
]


class Salary_elements(models.Model):
    class Meta:
        unique_together = [['emp', 'salary_month', 'salary_year', 'is_final']]

    emp = models.ForeignKey(Employee, on_delete=models.CASCADE,
                            null=True, blank=True, verbose_name=_('Employee'))
    salary_month = models.IntegerField(choices=month_name_choises, validators=[
        MaxValueValidator(12), MinValueValidator(1)], verbose_name=_('Salary Month'))
    salary_year = models.IntegerField(verbose_name=_('Salary Year'))
    run_date = models.DateField(auto_now=False, auto_now_add=False,
                                default=date.today, blank=True, null=True, verbose_name=_('Run Date'))
    element_batch = models.ForeignKey(
        Element_Batch, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Element Batch'))
    assignment_batch = models.ForeignKey(
        Assignment_Batch, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Assignment Batch'))
    ################################### Incomes/ allowances ####################
    incomes = models.FloatField(
        default=0.0, null=True, blank=True, verbose_name=_('Income'))
    ################################### Deductions #############################
    insurance_amount = models.FloatField(
        default=0.0, null=True, blank=True, verbose_name=_('Insurance Amount'))  # Deductions
    tax_amount = models.FloatField(
        default=0.0, null=True, blank=True, verbose_name=_('Tax Amount'))  # Deductions
    ############################################################################
    deductions = models.FloatField(
        default=0.0, null=True, blank=True, verbose_name=_('Deduction'))
    penalties = models.FloatField(
        default=0.0, null=True, blank=True, verbose_name=_('Penalties'))
    delays = models.FloatField(
        default=0.0, null=True, blank=True, verbose_name=_('Delays'))
    ############################################################################
    gross_salary = models.FloatField(
        default=0.0, null=True, blank=True, verbose_name=_('Gross Salary'))
    net_salary = models.FloatField(
        default=0.0, null=True, blank=True, verbose_name=_('Net Salary'))
    is_final = models.BooleanField(
        default=False, blank=True, verbose_name=_('Salary is final'))
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,
                                   on_delete=models.CASCADE, related_name="salary_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name="salary_last_update_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.emp.emp_name


@receiver(pre_save, sender=Salary_elements)
def employee_elements_history(sender, instance, *args, **kwargs):
    employee_old_elements = Employee_Element.objects.filter(emp_id=instance.emp)
    check_for_same_element = Employee_Element_History.objects.filter(emp_id=instance.emp_id,
                                                                     salary_month=instance.salary_month,
                                                                     salary_year=instance.salary_year)
    if check_for_same_element:
        for record in check_for_same_element:
            record.delete()
    else:
        for element in employee_old_elements:
            element_history = Employee_Element_History(
                emp_id=element.emp_id,
                element_id=element.element_id,
                element_value=element.element_value,
                salary_month=instance.salary_month,
                salary_year=instance.salary_year,
                creation_date=date.today(),
            )
            element_history.save()
