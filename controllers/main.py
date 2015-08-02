import webapp2
import pages
from config import *


class MainHandler(webapp2.RequestHandler):
    def get(self):
        view = pages.render_view(MAIN_URI)
        pages.render_page(self, view)


class ErrorHandler(webapp2.RequestHandler):
    def get(self):
        view = pages.render_view(ERROR_URI)
        pages.render_page(self, view)
