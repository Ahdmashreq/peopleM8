from django.contrib.auth.decorators import login_required
from notifications.views import AllNotificationsList


# I cant find where or how to make the changes I want withing the app's views.py, but this is an example
@login_required
def custom_get_queryset(self):
    # custom logic here, changing all notifications to 'read'

    return custom_get_queryset(self)


from django.shortcuts import render
