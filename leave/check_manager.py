from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save, post_init
from django.dispatch import receiver
from notifications.signals import notify
from .models import LeaveMaster, Leave, Employee_Leave_balance
from employee.models import JobRoll, Employee
from datetime import date
from django.utils.translation import ugettext_lazy as _
from .manager import LeaveManager
from company.models import Enterprise
from datetime import date, datetime
from custom_user.models import User

"""
Ziad
11/3/2021
Class to check manager and return employee manager
"""

class Check_Manager :

    def check_manger(emp):
        # get manger of employee
        employee_job = JobRoll.objects.get(end_date__isnull=True, emp_id=emp)
        if employee_job.manager:
            current_manger =[]
            current_manger.append(employee_job.manager)
        else:
             hr_users = User.objects.filter(groups__name='HR')
             hr_employees = Employee.objects.filter(user__in=hr_users)
             return hr_employees
        # get the leaves of manger
        in_leave = Leave.objects.filter(user=current_manger[0].user)
        if in_leave.exists() is True:
            # reverse the leaves to get the last leave
            # get end date of last leave
            end_date = in_leave.last().enddate
            start_date = in_leave.last().startdate
            today = date.today()
            status = in_leave.last().status
            # if in leave
            if start_date <= today <= end_date and status == "Approved":
                # get the parent manger
                employee_job = JobRoll.objects.filter(
                    end_date__isnull=True, emp_id=current_manger[0])
                # if not have parent manger "CEO"
                if not employee_job.exists():
                    return current_manger
                else:
                    # check if parent manger in leave or not
                    return self.check_manger(current_manger[0])
            else:
                # return the manger
                return current_manger
        return current_manger
 