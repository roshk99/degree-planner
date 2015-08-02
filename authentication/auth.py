"""
Application specific authentication module.
"""

import models.user
import webapp2
import json

from gaesessions import get_current_session
from config import *

import models.user


class RegisterResponseHandler(webapp2.RequestHandler):
    def post(self):
        data = json.loads(self.request.get('data'))
        user = models.user.create_user(data)
        if not user:
            self.response.out.write('This email is already in use')
        else:
            # Close any active session the user has since credentials have been freshly verified.
            session = get_current_session()
            if session.is_active():
                session.terminate()

            # Start a session for the user
            session['id'] = user['id']

            self.response.out.write('Success!')


class LoginResponseHandler(webapp2.RequestHandler):
    def post(self):
        data = json.loads(self.request.get('data'))
        user = models.user.check_user(data)

        if not user:
            self.response.out.write('Invalid Email/Password Combination')
        else:
            # Close any active session the user has since credentials have been freshly verified.
            session = get_current_session()
            if session.is_active():
                session.terminate()

            # Start a session for the user
            session['id'] = user['id']

            self.response.out.write('Success!')


class LogoutResponseHandler(webapp2.RequestHandler):
    def get(self):
        session = get_current_session()
        if 'id' in session:
            session.terminate()
            self.response.out.write('You\'ve been logged out. See you again soon!')
            self.redirect('/')
        else:
            self.response.out.write('You weren\'t logged in.')


def redirect_to_login(request_handler):
    """
    Requires the user to be logged in through NetID authentication.

    Args:
        request_handler: webapp2 request handler of the user request
    """
    request_handler.redirect(MAIN_URI, abort=True)


def get_logged_in_user():
    """
    Gets the logged in user.

    Returns:
        user: the user if logged in, None otherwise.
    """
    session = get_current_session()
    if 'id' in session:
        return models.user.get_user(session['id'])
    return None


def require_login(request_handler):
    """
    Requires the user to be logged in through NetID authentication.
    NOTE: Only works for non-AJAX GET requests.

    Args:
        request_handler: webapp2 request handler of the user request

    Returns:
        user: the database user object of the user logged in
    """
    user = get_logged_in_user()
    if not user:
        return redirect_to_login(request_handler)
    return user
