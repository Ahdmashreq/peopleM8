from element_definition.models import Element


class PayslipFunction(object):
    def get_element_amount_type(self, elm_id):
        try:
            element = Element.objects.get(id=elm_id)
            print(element.amount_type)
            return element.amount_type
        except:
            raise Exception("this field doesn't existed")

    def get_element_element_type(self, elm_id):
        try:
            element = Element.objects.get(id=elm_id)
            print(element.element_type)
            return element.element_type
        except:
            raise Exception("this field doesn't existed") 

    def get_element_scheduled_pay(self, elm_id):
        try:
            element = Element.objects.get(id=elm_id)
            print(element.scheduled_pay)
            return element.scheduled_pay
        except:
            raise Exception("this field doesn't existed")         

    def get_element_appears_on_payslip(self, elm_id):
        try:
            element = Element.objects.get(id=elm_id)
            print(element.appears_on_payslip)
            return element.appears_on_payslip
        except:
            raise Exception("this field doesn't existed")         
        