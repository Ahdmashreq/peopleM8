from django.contrib.sessions.models import Session
from django.conf import settings
from django import VERSION as DJANGO_VERSION
from django.utils import deprecation
from importlib import import_module
from django.contrib import messages
from custom_user.models import Visitor

engine = import_module(settings.SESSION_ENGINE)

def is_authenticated(user):
    """
    Check if user is authenticated, consider backwards compatibility
    """
    if DJANGO_VERSION >= (1, 10, 0):
        return user.is_authenticated
    else:
        return user.is_authenticated()


class PreventConcurrentLoginsMiddleware(deprecation.MiddlewareMixin if DJANGO_VERSION >= (1, 10, 0) else object):
    """
    Django middleware that prevents multiple concurrent logins..
    Adapted from http://stackoverflow.com/a/1814797 and https://gist.github.com/peterdemin/5829440
    """

    def process_request(self, request):
        if is_authenticated(request.user):
            new_logedin_session = request.session.session_key
            if hasattr(request.user, 'visitor'):
                old_session_key = request.user.visitor.session_key
                if old_session_key != new_logedin_session:
                    # Delete the Session object from database and cache
                    engine.SessionStore(old_session_key).delete()
                    request.user.visitor.session_key = new_logedin_session
                    request.user.visitor.save()
                    # messages.warning(request,'Your session has been expired.')
            else:
                django_session =Session.objects.get(session_key=new_logedin_session)
                Visitor.objects.create(
                    user=request.user,
                    session_key=new_logedin_session,
                )
