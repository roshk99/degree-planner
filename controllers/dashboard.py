import webapp2
import pages
import authentication.auth

from config import *


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = authentication.auth.get_logged_in_user()
        if not user:
            self.redirect(ERROR_URI)

        view = pages.render_view(DASHBOARD_URI)
        pages.render_page(self, view)
