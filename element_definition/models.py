from django.conf import settings
from django.db import models
from datetime import date
from manage_payroll.models import Payroll_Master
from company.models import (Enterprise, Department, Grade, Job, Position)
from defenition.models import LookupType, LookupDet
from django.utils.translation import ugettext_lazy as _


class Element_Batch(models.Model):
    payroll_fk = models.ForeignKey(Payroll_Master, on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name=_('Payroll'))
    batch_name = models.CharField(max_length=255, verbose_name=_('Batch Name'))
    start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, verbose_name=_('End Date'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="element_batch_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                       related_name="element_batch_last_update_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.batch_name


class SalaryStructure(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='enterprise_salary_structures',
                                   verbose_name=_('Enterprise Name'))
    structure_name = models.CharField(max_length=255, verbose_name=_('Structure Name'))
    start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, verbose_name=_('End Date'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="salary_structure_created_by")
    creation_date = models.DateField(auto_now=False, auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE,
                                       related_name="salary_structure_last_update_by")
    last_update_date = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.structure_name


class Element(models.Model):
    amount_type_choices = [('fixed amount', 'fixed amount'), ('percentage', 'percentage'), ('days', 'days'),
                           ('hrs', 'hrs'), ('months', 'months')]
    element_type_choices = [('payslip based', 'payslip based'), ('global value', 'global value'),
                            ('formula', 'formula')]
    scheduled_pay_choices = [('yearly', 'yearly'), ('monthly', 'monthly'), ('weekly', 'weekly')]

    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='enterprise_salary_elements',
                                   verbose_name=_('Enterprise Name'))
    element_name = models.CharField(max_length=100, verbose_name=_('Pay Name'))
    code = models.CharField(max_length=4, null=True, blank=True, verbose_name=_('code'))
    element_type = models.CharField(max_length=100, choices=element_type_choices)
    amount_type = models.CharField(max_length=100, choices=amount_type_choices)
    fixed_amount = models.IntegerField(default=0, verbose_name=_('Amount'), null=True, blank=True, )
    element_formula = models.TextField(max_length=255, null=True, blank=True, verbose_name=_('Formula'))
    based_on = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, )
    appears_on_payslip = models.BooleanField(verbose_name=_('Appears on payslip'), default=True)
    sequence = models.IntegerField(null=True, blank=True, )
    tax_flag = models.BooleanField(verbose_name=_('Tax Flag'), default=False)
    scheduled_pay = models.CharField(max_length=100, choices=scheduled_pay_choices)
    start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, verbose_name=_('End Date'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="element_is_created_by")
    creation_date = models.DateField(auto_now=False, auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       related_name="element_is_last_update_by", null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.element_name


class StructureElementLink(models.Model):
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.CASCADE, related_name='element_link', )
    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name='structure_link', )
    start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, verbose_name=_('End Date'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="link_is_created_by")
    creation_date = models.DateField(auto_now=False, auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE,
                                       related_name="link_is_last_update_by")
    last_update_date = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.salary_structure.structure_name + '.' + self.element.element_name


class Element_Master(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='enterprise_element_master',
                                   verbose_name=_('Enterprise Name'))
    element_name = models.CharField(max_length=100, verbose_name=_('Pay Name'))
    db_name = models.CharField(max_length=4, null=True, blank=True, verbose_name=_('db Name'))
    basic_flag = models.BooleanField(default=False)
    element_type = models.ForeignKey(LookupDet, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='lookup_element', verbose_name=_('Pay Type'))
    classification = models.ForeignKey(LookupDet, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='lookup_classification', verbose_name=_('classification'))
    effective_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today, null=True, blank=True,
                                      verbose_name=_('Effective Date'))
    retro_flag = models.BooleanField(verbose_name=_('Retro Flag'))
    tax_flag = models.BooleanField(verbose_name=_('Tax Flag'))
    fixed_amount = models.IntegerField(default=0, verbose_name=_('Fixed Amount'))
    element_formula = models.TextField(max_length=255, null=True, blank=True, verbose_name=_('Formula'))
    start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, verbose_name=_('End Date'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="element_master_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE,
                                       related_name="element_master_last_update_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.element_name


class Element_Batch_Master(models.Model):
    element_master_fk = models.ForeignKey(Element_Master, on_delete=models.CASCADE, null=True, blank=True,
                                          related_name='element_master_fk', related_query_name='elementMaster',
                                          verbose_name=_('Pay'))
    element_batch_fk = models.ForeignKey(Element_Batch, on_delete=models.CASCADE, null=True, blank=True,
                                         related_name='element_batch_fk', related_query_name='elementBatch',
                                         verbose_name=_('Pay Batch'))
    start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, verbose_name=_('End Date'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="element_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                       related_name="element_last_update_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.element_master_fk.element_name


class Element_Link(models.Model):
    class Meta:
        unique_together = ('element_master_fk', 'employee')

    element_master_fk = models.ForeignKey(Element_Master, on_delete=models.CASCADE, null=True, blank=True,
                                          related_name='element_link_to_master', verbose_name=_('Pay Name'))
    batch = models.ForeignKey(Element_Batch, on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name=_('Batch Name'))
    payroll_fk = models.ForeignKey(Payroll_Master, on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name=_('Payroll'))
    element_dept_id_fk = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True,
                                           verbose_name=_('Department'))
    element_job_id_fk = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Job'))
    element_grade_fk = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True, blank=True,
                                         verbose_name=_('Grade'))
    element_position_id_fk = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True,
                                               verbose_name=_('Position'))
    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name=_('Employee Name'))
    standard_flag = models.BooleanField(default=False, blank=True, verbose_name=_('Standard Flag'))
    link_to_all_payroll_flag = models.BooleanField(default=False, blank=True, verbose_name=_('Link All'))
    start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, verbose_name=_('End Date'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="element_link_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                       related_name="element_link_last_update_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        if self.element_master_fk:
            return self.element_master_fk.element_name
        else:
            return self.batch.batch_name


class Custom_Python_Rule(models.Model):
    default_string = '''
    You can define a custom deduction/addition rule here using python code.
    You have the following variables available to use:
    * basic: this is the basic salary of the employee.
    * variable: this is the variable salary of the employee.
    * d_days: these are the number of days the employee should be deducted this month
    because of his/her absence or any other Attendance rules that implies deduction days.
    * grs:(without `o`) gross salary equals to basic salary + variable salary + any other added allowances/bonus/incentive etc..
    After calculating your equation, you have to store the required amount to be added/deducted in a variable named amount.
    If the value of the amount variable is positive, the amount will be added to the net salary of the employee.
    And if it is negative, it will be deducted.
    Example:
    if basic <= 5000:
    ____extra_deduction = -250
    else:
    ____extra_deduction = -500
    amount = extra_deduction
    Make Sure that your code is properly indented using 4 spaces
    '''
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    element_master = models.ForeignKey(Element_Master, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='custom_python_rule', verbose_name=_('Pay Master'))
    help_text = models.TextField(default=default_string, verbose_name=_('Help Text'))
    rule_definition = models.TextField(verbose_name=_('Rule Definition'))
    taxable = models.BooleanField(default=False, verbose_name=_('Taxable'))

    def _ensure_no_syntax_errors(self):
        basic = 0.0
        variable = 0.0
        d_days = 0.0
        grs = 0.0

        try:
            exec(self.rule_definition)
        except Exception as e:
            msg = 'The code You have wrote produced the following error:\n "{}"'.format(e)
            raise ValidationError(msg)

    def _validate_custom_rule_security(self):
        danger = [
            'im_class', 'im_func', '__func__', 'im_self', '__self__', '__dict__', '__class__', 'func_closure',
            '__closure__', 'func_code', '__code__', 'func_defaults', '__defaults__', 'func_dict', 'func_doc',
            'func_globals', '__globals__', 'func_name', 'gi_code', 'gi_frame', 'import', 'os', 'system',
            'subprocess', '__', 'class', 'print', 'eval', 'exec', 'popen', 'sys', '__builtins__', '__name__',
            '__package__', '__cached__', '__doc__', '__file__', '__loader__', '__spec__', 're', 'run', 'self',
            'compile', 'builtins', 'locals', 'globals', '__module__', 'object', '__base__', '__subclasses__',
            'type', 'Popen',
        ]
        for word in danger:
            if word in self.rule_definition:
                msg = 'FOR SECURITY REASONS, YOU ARE NOT ALLOWED TO USE "{}" IN YOUR CODE!!'.format(word)
                raise ValidationError(msg)

    def clean(self):
        self._validate_custom_rule_security()
        self._ensure_no_syntax_errors()
        self.name = self.name.capitalize()

    def __str__(self):
        return self.name + "/" + self.company_id.name
