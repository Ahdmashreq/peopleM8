from django.conf import settings
from django.db import models
from django.urls import reverse
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from company.models import Department, Position
from employee.models import Employee


class Bussiness_Travel(models.Model):
    TRANSPORTATION_CHOICES = (('P','Plane'),('T','Train'),('B','Bus'),('C','Personal Car'))
    TRANSPORTATION_CHOICES_INSIDE=(('U','Uber'),('C','Car Rental'),('F','Ferry'),('O','Others'))
    ROOM_CHOICES=(('S','Single'),('D','Double'),('T','Triple'))
    accomodation_list = (('C','Company Accomodation'),('H','Hotel Accomodation'))
    # ##############################################################################################
    emp=models.ForeignKey(Employee, related_name='allowance_employee', on_delete=models.CASCADE,blank=True, null=True, verbose_name='Employee Name')
    manager = models.ForeignKey(Employee,related_name='allowance_manager', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Manager Name')
    date_requested= models.DateField(auto_now_add=True,editable=False, verbose_name='Date Requested')
    department=models.ForeignKey(Department, related_name='allowance_department', on_delete=models.CASCADE,blank=True, null=True, verbose_name='Department')
    position=models.ForeignKey(Position, related_name='parent_department', on_delete=models.CASCADE,blank=True, null=True, verbose_name='Position')
    destination=models.CharField(max_length=100,blank=True, null=True, verbose_name='Destination')
    estimated_date_of_travel_from= models.DateField(verbose_name='From Date')
    estimated_date_of_travel_to= models.DateField(verbose_name='To Date')
    prupose_of_trip=models.CharField(max_length=250,blank=True, null=True, verbose_name='Prupose Of Trip')
    project_name=models.CharField(max_length=100,blank=True, null=True, verbose_name='Project Name')
    transportation_type_to_des=models.CharField(max_length=1, choices=TRANSPORTATION_CHOICES, verbose_name='Transportation Type')
    ticket_cost=models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Ticket Cost')
    fuel_cost=models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Fuel Cost')
    transportation_type_in_city=models.CharField(max_length=1, blank=True, null=True,choices=TRANSPORTATION_CHOICES_INSIDE)
    cost=models.PositiveIntegerField(default=0, blank=True, null=True)
    accomodation=models.CharField(max_length=20, choices=accomodation_list, null=True ,blank=True, verbose_name='Accomodation')
    duration_of_hotel_from=models.DateField(blank=True, null=True)
    duration_of_hotel_to=models.DateField(blank=True, null=True)
    hotel_name=models.CharField(max_length=100,blank=True, null=True)
    cost_per_night=models.PositiveIntegerField(default=0, blank=True, null=True)
    status = models.CharField(max_length=20, default='pending')
    is_approved = models.BooleanField(default=False)

    status = models.CharField(max_length=12, default='pending')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='allowance_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       blank=True, null=True, related_name='allowance_last_updated_by')
    last_update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.emp.emp_name

class Purchase_Request(models.Model):
    payment_method_list = (('C','Cash'),('V','Visa'))
    # ##############################################################################################
    order_number = models.CharField(max_length=100,blank=True, null=True)
    ordered_by = models.ForeignKey(Employee, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    date_of_purchase = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name='Date Of Purchase')
    office = models.CharField(max_length=100,blank=True, null=True)
    payment_method = models.CharField(max_length=2, choices=payment_method_list, blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)
    vendor_details = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=12, default='pending', blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='purchase_request_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='purchase_request_last_updated_by')
    last_update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.ordered_by.emp_name

class Purchase_Item(models.Model):
    purchase_request = models.ForeignKey(Purchase_Request, on_delete=models.CASCADE)
    item_description = models.CharField(max_length=250,blank=True, null=True)
    vendor_name = models.CharField(max_length=250,blank=True, null=True)
    unit_price = models.PositiveIntegerField(default=0, blank=True, null=True)
    qnt = models.PositiveIntegerField(default=0, blank=True, null=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='purchase_item_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       blank=True, null=True, related_name='purchase_item_updated_by')
    last_update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.purchase_request.order_number
