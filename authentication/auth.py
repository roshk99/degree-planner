"""
Application specific authentication module.
"""

import logging
import webapp2
import json

from gaesessions import get_current_session
from config import *

import models.user
import models.semester


class RegisterResponseHandler(webapp2.RequestHandler):
    def post(self):
        data = json.loads(self.request.get('data'))
        user = models.user.create_user(data)

        user_model = models.user.get_user(user['id'])
        for num in range(SEMESTER_NUM):
            semester = models.semester.add_semester(user_model, num)
            if not semester:
                logging.info("There was an error creating semester number:" + num)
                return self.redirect(ERROR_URI)
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


class DeleteAccountHandler(webapp2.RequestHandler):
    def get(self):
        user = get_logged_in_user()
        if not user:
            self.redirect(ERROR_URI)

        session = get_current_session()
        if 'id' in session:
            session.terminate()
            self.redirect('/')

        # Delete all semesters
        semesters = models.semester.get_semesters_for_user(user)
        for semester in semesters:
            semester_model = models.semester.get_semester(semester['id'])
            models.semester.delete_semester(semester_model)

        models.user.delete_user(user)


def redirect_to_login(request_handler):
    """
    Requires the user to be logged in through NetID authentication.

    Args:
        request_handler: webapp2 request handler of the user request
    """
    request_handler.redirect('/', abort=True)


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
