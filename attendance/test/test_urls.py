from django.test import SimpleTestCase
from django.urls import resolve, reverse
from attendance.views import list_attendance, check_in_time, check_out_time, create_task

class TestUrls(SimpleTestCase):

    def test_list_attendance_url_resolves(self):
        url = reverse("attendance:user-list-attendance")
        self.assertEquals(resolve(url).func, list_attendance)
