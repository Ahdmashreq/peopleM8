from element_definition.models import Element_Master


class FastFormula:

    def __init__(self, emp_id, element_id, class_name):
        self.emp_id = emp_id
        self.element_id = element_id
        self.class_name = class_name

    def _convert_formula(self, str):
        output = ''
        for x in str:
            if x == "+" or x == "-" or x == "*" or x == "/":
                x = " {} ".format(x)
            if x == "%":
                x = "/100"
            output += x
        return output

    def get_emp_elements(self):
        # get all elements for one employee and put them in a dic
        emp_elements = self.class_name.objects.filter(emp_id=self.emp_id)
        return emp_elements

    def get_fast_formula(self):
        # return a dic contains all the formula elements from the master element table.
        # formula_elements = ElementMaster.objects.filter().exclude(element_formula__exact="")
        formula_elements = self.class_name.objects.filter(emp_id=self.emp_id, element_id=self.element_id)
        formulas = {}
        for x in formula_elements:
            formulas.update({self._convert_formula(
                x.element_id.element_formula): x.element_id.id})
        return formulas

    def get_formula_amount(self):
        # will check first if the employee have the formula element,
        # then we do calculations based on his elements.
        amount = 0
        for x in self.get_emp_elements():
            custom_rule = ''
            ldict = {}
            for key in self.get_fast_formula():  # looping in fast formula dic to check if the user have this FF
                custom_rule = "amount = " + key
                for i in custom_rule.split():
                    if i == x.element_id.code and x.element_id.basic_flag == False:
                        element_value = x.element_value
                        custom_rule = custom_rule.replace(i, str(element_value))
                        ldict = locals()
                        exec(custom_rule, globals(), ldict)
                        amount = ldict['amount']
        return amount
