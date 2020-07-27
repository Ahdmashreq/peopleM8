from notification.models import Notification
from leave.models import Leave
from service.models import Bussiness_Travel, Purchase_Request

class NotificationHelper:
    def __init__(self, from_emp, to_emp, obj):
        self.from_emp = from_emp
        self.to_emp = to_emp
        self.obj = obj

    def send_notification(self):
        if isinstance(self.obj,Leave):
            notification_obj = Notification(
                from_emp=self.from_emp,
                to_emp=self.to_emp,
                message="Employee {} asks for a leave.".format(self.from_emp),
                leave=self.obj
            )
            notification_obj.save()
            return True
        elif isinstance(self.obj,Bussiness_Travel):
            notification_obj = Notification(
                from_emp=self.from_emp,
                to_emp=self.to_emp,
                message="Employee {} requested a bussiness travel. and need your approve".format(self.from_emp),
                bussiness_travel = self.obj
            )
            notification_obj.save()
            return True
        else:
            notification_obj = Notification(
                from_emp=self.from_emp,
                to_emp=self.to_emp,
                message="Employee {} requested a purchase order. and need your approve".format(self.from_emp),
                Purchase_Request = self.obj
            )
            notification_obj.save()
            return True
        return False
