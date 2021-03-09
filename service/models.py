from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from notifications.signals import notify

from company.models import Department, Position
from employee.models import Employee , JobRoll
from custom_user.models import User


class Bussiness_Travel(models.Model):
    TRANSPORTATION_CHOICES = (('P', 'Plane'), ('T', 'Train'), ('B', 'Bus'), ('C', 'Personal Car'))
    TRANSPORTATION_CHOICES_INSIDE = (('U', 'Uber'), ('C', 'Car Rental'), ('F', 'Ferry'), ('O', 'Others'))
    ROOM_CHOICES = (('S', 'Single'), ('D', 'Double'), ('T', 'Triple'))
    accomodation_list = (('C', 'Company Accomodation'), ('H', 'Hotel Accomodation'))
    # ##############################################################################################
    emp = models.ForeignKey(Employee, related_name='allowance_employee', on_delete=models.CASCADE, blank=True,
                            null=True, verbose_name='Employee Name')
    manager = models.ForeignKey(Employee, related_name='allowance_manager', on_delete=models.CASCADE, blank=True,
                                null=True, verbose_name='Manager Name')
    date_requested = models.DateField(auto_now_add=True, editable=False, verbose_name='Date Requested')
    department = models.ForeignKey(Department, related_name='allowance_department', on_delete=models.CASCADE,
                                   blank=True, null=True, verbose_name='Department')
    position = models.ForeignKey(Position, related_name='parent_department', on_delete=models.CASCADE, blank=True,
                                 null=True, verbose_name='Position')
    destination = models.CharField(max_length=100, blank=True, null=True, verbose_name='Destination')
    estimated_date_of_travel_from = models.DateField(verbose_name='From Date')
    estimated_date_of_travel_to = models.DateField(verbose_name='To Date')
    prupose_of_trip = models.CharField(max_length=250, blank=True, null=True, verbose_name='Prupose Of Trip')
    project_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Project Name')
    transportation_type_to_des = models.CharField(max_length=1, choices=TRANSPORTATION_CHOICES,
                                                  verbose_name='Transportation Type')
    ticket_cost = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Ticket Cost')
    fuel_cost = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Fuel Cost')
    transportation_type_in_city = models.CharField(max_length=1, blank=True, null=True,
                                                   choices=TRANSPORTATION_CHOICES_INSIDE)
    cost = models.PositiveIntegerField(default=0, blank=True, null=True)
    accomodation = models.CharField(max_length=20, choices=accomodation_list, null=True, blank=True,
                                    verbose_name='Accomodation')
    duration_of_hotel_from = models.DateField(blank=True, null=True)
    duration_of_hotel_to = models.DateField(blank=True, null=True)
    hotel_name = models.CharField(max_length=100, blank=True, null=True)
    cost_per_night = models.PositiveIntegerField(default=0, blank=True, null=True)
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
        return 'Business Travel'


class Purchase_Request(models.Model):
    payment_method_list = (('C', 'Cash'), ('V', 'Visa'))
    # ##############################################################################################
    order_number = models.CharField(max_length=100, blank=True, null=True)
    ordered_by = models.ForeignKey(Employee, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    date_of_purchase = models.DateField(auto_now=False, auto_now_add=False, default=date.today,
                                        verbose_name='Date Of Purchase')
    office = models.CharField(max_length=100, blank=True, null=True)
    payment_method = models.CharField(max_length=2, choices=payment_method_list, blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)
    vendor_details = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=12, default='pending', blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='purchase_request_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       related_name='purchase_request_last_updated_by')
    last_update_date = models.DateField(auto_now=True)

    def __str__(self):
        return 'Purchase Request'


class Purchase_Item(models.Model):
    purchase_request = models.ForeignKey(Purchase_Request, on_delete=models.CASCADE)
    item_description = models.CharField(max_length=250, blank=False, null=False)
    vendor_name = models.CharField(max_length=250, blank=False, null=False)
    unit_price = models.PositiveIntegerField(blank=False, null=False)
    qnt = models.PositiveIntegerField(blank=False, null=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='purchase_item_created_by')
    creation_date = models.DateField(auto_now_add=True)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       blank=True, null=True, related_name='purchase_item_updated_by')
    last_update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.purchase_request.order_number


@receiver(post_save, sender=Bussiness_Travel)
def business_request_handler(sender, instance, created, update_fields, **kwargs):
    """
           This function is a receiver, it listens to any save hit on Business_Travel model, and send
           a notification to the manager that someone created a Business_Travel request,
           or send a notification to the person who created the Travel, if his request is processed .
    """
    requestor_emp = instance.emp
    required_job_roll = JobRoll.objects.get(emp_id = instance.emp.id, end_date__isnull=True)
    if required_job_roll.manager:
        manager_emp = required_job_roll.manager.user
    else:
        hr_users = User.objects.filter(groups__name='HR')
        manager_emp = hr_users

    if created:  # check if this is a new Business_travel instance
        data = {"title": "Business Travel Request", "status": instance.status, "href": "service:services_edit"}
        notify.send(sender=requestor_emp.user,
                    recipient=manager_emp,
                    verb='requested', action_object=instance,
                    description="{employee} requested a Business Travel".format(employee=requestor_emp), level='action',
                    data=data)
    elif 'status' in update_fields:  # check if Business travel status is updated
        data = {"title": "Business Travel Request", "status": instance.status}

        # send notification to the requestor employee that his request status is updated
        notify.send(sender=manager_emp,
                    recipient=requestor_emp.user,
                    verb=instance.status, action_object=instance,
                    description="{employee} has {status} your Business Travel request".format(employee=manager_emp,
                                                                                              status=instance.status),
                    level='info',
                    data=data)

        #  update the old notification for the manager with the new status
        content_type = ContentType.objects.get_for_model(Bussiness_Travel)
        old_notification = manager_emp.user.notifications.filter(action_object_content_type=content_type,
                                                                 action_object_object_id=instance.id)
        if len(old_notification) > 0:
            old_notification[0].data['data']['status'] = instance.status
            old_notification[0].data['data']['href'] = ""
            old_notification[0].unread = False
            old_notification[0].save()


@receiver(post_save, sender=Purchase_Request)
def purchase_request_handler(sender, instance, created, update_fields, **kwargs):
    """
       This function is a receiver, it listens to any save hit on Purchase_Request model, and send
       a notification to the manager that someone created a Purchase_Request request,
       or send a notification to the person who created the request, if his request is processed .
    """
    requestor_emp = instance.ordered_by
    required_job_roll = JobRoll.objects.get(emp_id = instance.ordered_by, end_date__isnull=True)
    if required_job_roll.manager:
        manager_emp = required_job_roll.manager.user
    else:
        hr_users = User.objects.filter(groups__name='HR')
        manager_emp = hr_users
    if created:  # check if this is a new Purchase_Request instance
        data = {"title": "Purchase Request", "status": instance.status, "href": "service:purchase-request-update"}

        notify.send(sender=requestor_emp.user,
                    recipient=manager_emp,
                    verb='created a', action_object=instance,
                    description="{employee} has created a purchase request".format(employee=requestor_emp),
                    level='action',
                    data=data)
    elif 'status' in update_fields:  # check if Purchase_Request status is updated
        data = {"title": "Purchase Request", "status": instance.status}

        # send notification to the requestor employee that his request status is updated
        notify.send(sender=manager_emp.user,
                    recipient=instance.ordered_by.user,
                    verb=instance.status, action_object=instance,
                    description="{employee} has {status} your purchase request".format(employee=manager_emp,
                                                                                       status=instance.status),
                    level='info', data=data)

        #  update the old notification for the manager with the new status
        content_type = ContentType.objects.get_for_model(Purchase_Request)
        old_notification = manager_emp.user.notifications.filter(action_object_content_type=content_type,
                                                                 action_object_object_id=instance.id)
        if len(old_notification) > 0:
            old_notification[0].data['data']['status'] = instance.status
            old_notification[0].data['data']['href'] = ""
            old_notification[0].unread = False
            old_notification[0].save()
