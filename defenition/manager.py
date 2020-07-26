from django.db import models
from django.db.models import Q
from datetime import date, datetime

class LookupTypeManager(models.Manager):
    def all(self,user, *args, **kwargs):
        return super(LookupTypeManager, self).filter((Q(enterprise__enterprise_user = user) | Q(enterprise=1))).filter(Q(end_date__gte=date.today())|Q(end_date__isnull=True))

    def get_lookup(self,user,lookup_id, *args, **kwargs):
        return super(LookupTypeManager, self).filter((Q(enterprise__enterprise_user = user) | Q(enterprise=1))).filter(Q(end_date__gte=date.today())|Q(end_date__isnull=True)).get(id=lookup_id)

class InsuranceRuleManager(models.Manager):
    def all(self,user, *args, **kwargs):
        return super(InsuranceRuleManager, self).filter((Q(enterprise_name__enterprise_user = user) | Q(enterprise_name=1))).filter(Q(end_date__gte=date.today())|Q(end_date__isnull=True))

    def get_insuracne(self,user,insuracne_id, *args, **kwargs):
        return super(InsuranceRuleManager, self).filter((Q(enterprise_name__enterprise_user = user) | Q(enterprise_name=1))).filter(Q(end_date__gte=date.today())|Q(end_date__isnull=True)).get(id=insuracne_id)

class TaxRuleManager(models.Manager):
    def all(self,user, *args, **kwargs):
        return super(TaxRuleManager, self).filter((Q(enterprise__enterprise_user = user) | Q(enterprise=1))).filter(Q(end_date__gte=date.today())|Q(end_date__isnull=True))

    def get_tax(self,user,tax_id, *args, **kwargs):
        return super(TaxRuleManager, self).filter((Q(enterprise__enterprise_user = user) | Q(enterprise=1))).filter(Q(end_date__gte=date.today())|Q(end_date__isnull=True)).get(id=tax_id)
