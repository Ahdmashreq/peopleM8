from django.db.models import Q
from company.models import Working_Days_Policy, YearlyHoliday
from leave.models import Leave
from service.models import Bussiness_Travel
import calendar


def is_day_a_leave(user_id, day):
    leaves = Leave.objects.filter(
        Q(user__id=user_id) & ((Q(startdate__month=day.month) & Q(startdate__year=day.year)) | (
                Q(enddate__month=day.month) and Q(enddate__year=day.year))), status='Approved')
    for leave in leaves:
        if leave.startdate <= day <= leave.enddate:
            return True
    return False


def is_day_a_service(employee_id, day):
    services = Bussiness_Travel.objects.filter(
        Q(emp__id=employee_id) & (
                (Q(estimated_date_of_travel_from__month=day.month) & Q(
                    estimated_date_of_travel_from__year=day.year)) | (
                        Q(estimated_date_of_travel_to__month=day.month) & Q(
                    estimated_date_of_travel_from__year=day.year))), status='Approved')
    for service in services:
        if service.estimated_date_of_travel_from <= day <= service.estimated_date_of_travel_to:
            return True
    return False


def is_day_a_holiday(day):
    month_holidays = YearlyHoliday.objects.filter(
        Q(year=day.year) & (Q(start_date__month=day.month) |
                            Q(end_date__month=day.month))).values('start_date',
                                                                  'end_date')
    for x in month_holidays:
        if x.start_date <= day <= x.end_date:
            return True
    return False


def is_day_a_weekend(day):
    weekends = Working_Days_Policy.objects.values('week_end_days')
    day_name = calendar.day_name[day.weekday()]
    if day_name.upper() in weekends[0]['week_end_days']:
        return True
    else:
        return False
