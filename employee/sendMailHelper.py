from django.core.mail import send_mail
from django.template import loader


class SendMail:
    def __init__(self, service_type_v, employee_v, employee_job_v=None, leav_v=None,
                 leave_start_date=None, leave_end_date=None,
                 leave_resume_date=None, reason_v=None, ):
        self.service_type_v = service_type_v
        self.employee_v = employee_v
        self.employee_job_v = employee_job_v
        self.leav_v = leav_v
        self.leave_start_date = leave_start_date
        self.leave_end_date = leave_end_date
        self.leave_resume_date = leave_resume_date
        self.reason_v = reason_v

    def sendMailToOne():
        requestor = employee
        requestor_email = employee.email
        leave_type = leave.leavetype
        from_date = leave.startdate
        to_date =	leave.enddate
        resume = leave.resume_date
        reason =	leave.reason
        team_leader =	employee_job.manager
        team_leader_email =	employee_job.manager.email
        mail_body = '''
        dear {6}
            Employee {0} submitting for a {1} leave.
            Leave start from {2} to {3} and will resumde duty on {4}.
        The employee have the following reasons:
            {5}

        '''
        send_mail(
            'Mashreq Arabia Leave Form',
            mail_body.format(requestor,leave_type,from_date, to_date, resume, reason, team_leader),
            requestor_email,
            [team_leader_email],
            fail_silently=False,
        )
