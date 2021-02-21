from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
from defenition.models import LookupType, LookupDet
from company.models import (Enterprise, Department, Grade, Position, Job)
from employee.fast_formula import FastFormula
from manage_payroll.models import (Bank_Master, Payroll_Master)
import element_definition.models
from django_cryptography.fields import encrypt

payment_type_list = [("c", _("Cash")), ("k", _("Check")),
                     ("b", _("Bank transfer")), ]
account_type_list = [('c', _('Company account')), ('e', _('Employee account'))]


class Employee(models.Model):
    identification_type_list = [("N", _("National Id")), ("P", _("Passport"))]
    gender_list = [("M", _("Male")), ("F", _("Female"))]
    social_status_list = [("M", _("Married")), ("S", _("Single"))]
    military_status_list = [("E", _("Exemption")), ("C", _(
        "Complete the service")), ("P", _("Postponed"))]
    religion_list = [("M", _("Muslim")), ("C", _("Chrestin"))]
    emp_type_list = [("UP", _("Under Probation")), ("E", _("Employee")), ("EX", _("Ex-Employee")),
                     ("C", _("Contractor"))]
    # ##########################################################################
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                             related_name='employee_user')
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='enterprise_employee',
                                   verbose_name=_('Department'))
    emp_number = models.IntegerField(
        default=0, blank=True, null=True, verbose_name=_('Employee Number'))
    emp_type = models.CharField(max_length=30, choices=emp_type_list, null=True, blank=True,
                                verbose_name=_('Employee Type'))
    emp_name = models.CharField(max_length=60, verbose_name=_('Employee Name'))
    address1 = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_('address1'))
    address2 = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_('address2'))
    phone = models.CharField(max_length=255, blank=True,
                             null=True, verbose_name=_('phone'))
    mobile = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_('mobile'))
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,
                                     verbose_name=_('Birthdate'))
    hiredate = models.DateField(
        auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Hire Date'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('email'))
    picture = models.ImageField(
        null=True, blank=True, verbose_name=_('picture'))
    is_active = models.BooleanField(
        blank=True, default=True, verbose_name=_('Is Active'))
    identification_type = models.CharField(max_length=5, choices=identification_type_list, null=True, blank=True,
                                           verbose_name=_('ID Type'))
    id_number = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_('ID Number'))
    place_of_birth = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=_('Place of Birth'))
    nationality = models.CharField(
        max_length=20, blank=True, null=True, verbose_name=_('Nationality'))
    field_of_study = models.CharField(
        max_length=30, blank=True, null=True, verbose_name=_('Field of Study'))
    education_degree = models.CharField(
        max_length=30, blank=True, null=True, verbose_name=_('Eductaion Degree'))
    gender = models.CharField(
        max_length=5, choices=gender_list, null=True, blank=True, verbose_name=_('Gender'))
    social_status = models.CharField(max_length=5, choices=social_status_list, null=True, blank=True,
                                     verbose_name=_('Social Status'))
    military_status = models.CharField(max_length=5, choices=military_status_list, null=True, blank=True,
                                       verbose_name=_('Milatery Status'))
    religion = models.CharField(
        max_length=5, choices=religion_list, null=True, blank=True, verbose_name=_('Religion'))
    insured = models.BooleanField(verbose_name=_('Insured'))
    insurance_number = models.CharField(
        max_length=30, blank=True, null=True, verbose_name=_('Insurance Number'))
    insurance_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,
                                      verbose_name=_('Insurance Date'))
    insurance_salary = models.FloatField(
        default=0.0, null=True, blank=True, verbose_name=_('Insurance Salary'))
    has_medical = models.BooleanField(verbose_name=_('Has Medical'))
    medical_number = models.CharField(
        max_length=30, blank=True, null=True, verbose_name=_('Medical Number'))
    medical_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,
                                    verbose_name=_('Medical Date'))
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="emp_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def get_absolute_url(self):
        return reverse("list-employee", kwargs={"pk": self.id})

    def __str__(self):
        return self.emp_name


class Medical(models.Model):
    emp_id = models.ForeignKey(
        Employee, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Employee'))
    medical_code = models.CharField(
        max_length=20, verbose_name=_('Medical Code'))
    medical_name = models.CharField(
        max_length=20, verbose_name=_('Medical Name'))
    medical_company = models.CharField(
        max_length=20, verbose_name=_('Medical Company'))
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="medical_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,
        related_name="medical_last_update_by")

    def __str__(self):
        return self.emp_id.emp_name


class JobRoll(models.Model):
    emp_type_list = [("A", _("Admin")),
                     ("E", _("Employee"))]
    # ###########################################################################################
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE,
                               null=True, blank=True, related_name='job_roll_emp_id', verbose_name=_('Employee'))
    manager = models.ForeignKey(
        Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='manager_id', verbose_name=_('Manager'))
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Position'))
    contract_type = models.ForeignKey(LookupDet, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='jobroll_contract_type', verbose_name=_('Contract Type'))
    payroll = models.ForeignKey(Payroll_Master, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name=_('Payroll'))
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="jobRoll_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,
        related_name="jobroll_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)


class Payment(models.Model):
    emp_id = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name=_('Employee'))
    payment_method = models.ForeignKey(
        'manage_payroll.Payment_Method', on_delete=models.CASCADE, related_name='emp_payment_method',
        verbose_name=_('Payment Method'))
    account_number = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_('Account Number'))
    percentage = models.IntegerField(default=100, validators=[
        MaxValueValidator(100), MinValueValidator(0)], verbose_name=_('Percentage'))
    bank_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_('Bank Name'))
    swift_code = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_('Swift Code'))
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payment_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,
        related_name="payment_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.payment_method.payment_type.type_name


class Employee_Element(models.Model):
    emp_id = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name=_('Employee'))
    element_id = models.ForeignKey(
        element_definition.models.Element, on_delete=models.CASCADE, verbose_name=_('Pay'))
    element_value =encrypt(models.FloatField(
        default=0.0, null=True, blank=True, verbose_name=_('Pay Value')))
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="emp_element_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name="emp_element_last_update_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.element_id.element_name

    @receiver(post_save, sender='employee.Employee_Element')
    # this receiver is used to delete all records with end dates have come so they are not put in history
    def delete_links_with_due_end_date(sender, instance, **kwargs):
        if instance.end_date is not None and instance.end_date <= date.today():
            instance.delete()

    # def set_formula_amount(emp):
    #     formula_element = Employee_Element.objects.filter(emp_id=emp.id, element_id__element_formula__isnull=False)
    #     for x in formula_element:
    #         if x.element_value is None:
    #             x.element_value = 0
    #             x.save()
    #         if x.element_value == 0:
    #             value = FastFormula(emp.id, x.element_id, Employee_Element)
    #             x.element_value = value.get_formula_amount()
    #             x.save()

    def get_element_value(self):
        element_dic = {}
        element_master_obj = element_definition.models.Element.objects.filter().exclude(fixed_amount=0)
        for element in element_master_obj:
            element_dic[element.id] = (element.fixed_amount)
        emp_elements = Employee_Element.objects.filter(emp_id=self.emp_id)
        for element in element_dic:
            if self.element_id.id == element:
                self.element_value = element_dic[element]

    def save(self):
        # self.get_element_value()
        super().save()


class EmployeeStructureLink(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, )
    salary_structure = models.ForeignKey(element_definition.models.SalaryStructure, on_delete=models.CASCADE,
                                         related_name='employee_structure_link', )
    start_date = models.DateField(
        auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True, verbose_name=_('End Date'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                   related_name="employee_salary_is_created_by")
    creation_date = models.DateField(auto_now=False, auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE,
                                       related_name="employee_salary_is_last_update_by")
    last_update_date = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.employee.emp_name + ' ' + self.salary_structure.structure_name

    @receiver(pre_save, sender='employee.EmployeeStructureLink')
    def insert_employee_elements(sender, instance, *args, **kwargs):
        if instance.id is not None:  # if record is being updated
            # delete elements related to old structure in emp-elements
            old_salary_structure_link = EmployeeStructureLink.objects.get(
                id=instance.id)
            linked_elements = element_definition.models.StructureElementLink.objects.filter(
                salary_structure=old_salary_structure_link.salary_structure).filter(
                Q(end_date__isnull=True) | Q(end_date__gt=date.today())).values('element')
            employee_elements = Employee_Element.objects.filter(emp_id=instance.employee,
                                                                element_id__in=linked_elements)
            for emp_el in employee_elements:
                emp_el.delete()

        required_salary_structure = instance.salary_structure
        elements_in_structure = element_definition.models.StructureElementLink.objects.filter(
            salary_structure=required_salary_structure,
            end_date__isnull=True)
        for element in elements_in_structure:
            employee_element_obj = Employee_Element(
                emp_id=instance.employee,
                element_id=element.element,
                element_value=element.element.fixed_amount,
                start_date=instance.start_date,
                end_date=instance.end_date,
                created_by=instance.created_by,
                last_update_by=instance.last_update_by,
            )
            employee_element_obj.save()


month_name_choises = [
    (1, _('January')), (2, _('February')), (3, _('March')), (4, _('April')),
    (5, _('May')), (6, _('June')), (7, _('July')), (8, _('August')),
    (9, _('September')), (10, _('October')
                          ), (11, _('November')), (12, _('December')),
]


class Employee_Element_History(models.Model):
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE, )
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    element_id = GenericForeignKey()
    salary_month = models.IntegerField(choices=month_name_choises, validators=[
        MaxValueValidator(12), MinValueValidator(1)], verbose_name=_('Salary Month'), default=date.today().month)
    salary_year = models.IntegerField(verbose_name=_(
        'Salary Year'), default=date.today().year)
    element_value = models.FloatField(default=0.0, null=True, blank=True)
    element_computed_value = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    start_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True,
                                  verbose_name=_('Start Date'))
    end_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,
                                   related_name="emp_element_history_created_by")
    creation_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, )
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name="emp_element_history_last_update_by")
    last_update_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True, )

    def __str__(self):
        return self.emp_id.emp_name + ' / ' + self.element_id.element_name
