from django.conf import settings
from django.db import models
from datetime import date
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import pre_save
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
    num_days = models.FloatField(
        default=0.0, null=True, blank=True, verbose_name=_('Number of Days'))
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
        settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="salary_last_update_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def _get_insured_emp_basic(self):
        emp_element = Employee_Element.objects.filter(
            emp_id=self.emp, element_id__db_name='001', emp_id__insured=1).filter((Q(end_date__gte=date.today()) | Q(end_date__isnull=True)))
        emp_basic = 0.0
        for x in emp_element:
            emp_basic += x.element_value
        return emp_basic

    def _get_uninsured_emp_basic(self):
        emp_element = Employee_Element.objects.filter(
            emp_id=self.emp, element_id__db_name='001', emp_id__insured=0).filter(
                (Q(end_date__gte=date.today()) | Q(end_date__isnull=True)))
        emp_basic = 0.0
        for x in emp_element:
            emp_basic += x.element_value
        return emp_basic

    def _get_emp_income(self):
        emp_allowance = Employee_Element.objects.filter(element_id__classification__code='earn', emp_id=self.emp).filter(
            (Q(end_date__gte=date.today()) | Q(end_date__isnull=True)))
        self.incomes = 0
        for x in emp_allowance:
            self.incomes += x.element_value
        return self.incomes

    def _get_emp_deduction_elements(self):
        emp_deductions = Employee_Element.objects.filter(
            element_id__classification__code='deduct', emp_id=self.emp).filter(
                (Q(end_date__gte=date.today()) | Q(end_date__isnull=True)))
        self.deductions = 0
        for x in emp_deductions:
            self.deductions += x.element_value
        return self.deductions

    def _calc_all_incomes(self):
        total_incomes = (
            self._get_emp_income()
        )
        return total_incomes

    def _calc_all_deductions(self):
        total_deductions = (
            self._get_emp_deduction_elements()
        )
        return total_deductions

    def _calc_variable_salary(self):
        if self.emp.insured == 1:
            total_variable = (self._calc_all_incomes() -
                              self._get_insured_emp_basic())
        else:
            total_variable = (self._calc_all_incomes() -
                              self._get_uninsured_emp_basic())
        return total_variable

    def _calc_insurance(self):
        if self.emp.insured == 1:
            insurance_rule_master = Payroll_Master.objects.get()
            constant_amount_ratio = insurance_rule_master.social_insurance.basic_deduction_percentage / 100
            variable_amount_ratio = insurance_rule_master.social_insurance.variable_deduction_percentage / 100
            if self._get_insured_emp_basic() <= insurance_rule_master.social_insurance.maximum_insurable_basic_salary:
                constant_amount = self._get_insured_emp_basic() * constant_amount_ratio
            else:
                constant_amount = insurance_rule_master.social_insurance.maximum_insurable_basic_salary * \
                    constant_amount_ratio
            if self._calc_variable_salary() <= insurance_rule_master.social_insurance.maximum_insurable_variable_salary:
                variable_amount = self._calc_variable_salary() * variable_amount_ratio
            else:
                variable_amount = insurance_rule_master.social_insurance.maximum_insurable_variable_salary * \
                    variable_amount_ratio
            insurance_deduction = constant_amount + variable_amount
            self.insurance_amount = insurance_deduction
            return round(insurance_deduction, 2)
        else:
            return 0.0

    def _calc_taxes_deduction(self):
        tax_rule_master = Payroll_Master.objects.get()
        personal_exemption = tax_rule_master.tax_rule.personal_exemption
        round_to_10 = tax_rule_master.tax_rule.round_down_to_nearest_10
        tax_deduction_amount = Tax_Deduction_Amount(
            personal_exemption, round_to_10)
        taxable_salary = self._calc_gross_salary()
        taxes = tax_deduction_amount.run_tax_calc(taxable_salary)
        self.tax_amount = taxes
        return round(taxes, 2)

    def _calc_gross_salary(self):
        self.gross_salary = self._calc_all_incomes() - self._calc_all_deductions() - \
            self._calc_insurance()
        return self.gross_salary

    def _calc_net_salary(self):
        self.net_salary = self._calc_gross_salary() - self._calc_taxes_deduction()
        return self.net_salary

    def _validate_is_latest_record(self):
        later_records = Salary_elements.objects.filter(
            salary_month__gte=self.salary_month).filter(salary_year__gte=self.salary_year).filter(is_final=True)
        if len(later_records) > 0:
            raise ValidationError(
                _('There is another Salary record that is later than this one'), code='invalid_date')

    def _recalculate_salary(self):
        get_salary = Salary_elements.objects.filter(salary_month=self.salary_month,
                                                    salary_year=self.salary_year,
                                                    is_final=self.is_final,
                                                    element_batch=self.element_batch,
                                                    assignment_batch=self.assignment_batch)
        for x in get_salary:
            x.delete()

    def clean(self):
        self._validate_is_latest_record()
        self._recalculate_salary()

    def save(self):
        self._calc_net_salary()
        super().save()

    def __str__(self):
        return self.emp.emp_name


@receiver(pre_save, sender=Salary_elements)
def employee_elements_history(sender, instance, *args, **kwargs):
    employee_old_elements = Employee_Element.objects.filter(emp_id=instance.emp)
    check_for_element = Employee_Element_History.objects.filter(employee=instance.emp_id, salary_month=instance.salary_month, salary_year=instance.salary_year)
    if len(check_for_element) > 0:
        for record in check_for_element:
            record.delete()
    for element in employee_old_elements:
        element_history = Employee_Element_History(
                                 employee = element.emp_id,
                                 element = element.element_id,
                                 element_value = element.element_value,
                                 salary_month = instance.salary_month,
                                 salary_year = instance.salary_year,
                                 creation_date = date.today(),
        )
        element_history.save()
    
