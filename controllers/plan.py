import pages
import webapp2
from config import *


class MainHandler(webapp2.RequestHandler):
    def get(self):
        view = pages.render_view(PLAN_URI)
        pages.render_page(self, view)
