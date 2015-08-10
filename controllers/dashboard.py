import webapp2
import pages
import authentication.auth

from config import *

import models.user
import models.semester
import models.course
import models.university
import models.major
import models.requirement
import utils.utils


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = authentication.auth.get_logged_in_user()
        if not user:
            authentication.auth.redirect_to_login(self)

        university = models.university.get_university(user.get_university()).to_json()
        semesters = models.semester.get_semesters_for_user(user)

        all_courses = {}
        for semester in semesters:
            all_courses[int(semester['number'])] = utils.utils.semester_as_list(semester['courses'])

        my_university = university['name']
        my_majors = utils.utils.majors_as_text(user.get_majors())

        all_majors = models.major.get_majors_for_university(university['id'])

        view = pages.render_view(DASHBOARD_URI, {'first_name': user.get_first_name(),
                                                 'last_name': user.get_last_name(),
                                                 'email': user.get_email(),
                                                 'my_university': my_university,
                                                 'my_majors': my_majors,
                                                 'my_courses': all_courses,
                                                 'all_majors': all_majors})
        pages.render_page(self, view)


class AddMajorHandler(webapp2.RequestHandler):
    def post(self):
        user = authentication.auth.get_logged_in_user()
        if not user:
            authentication.auth.redirect_to_login(self)

        major_id = self.request.get('id')

        result = models.user.add_major(user, major_id)
        if not result:
            self.response.out.write('Already added!')
        else:
            self.response.out.write('Success')


class ClearMajorsHandler(webapp2.RequestHandler):
    def get(self):
        user = authentication.auth.get_logged_in_user()
        if not user:
            authentication.auth.redirect_to_login(self)

        models.user.clear_majors(user)

        # Delete all classes in semesters
        semesters = models.semester.get_semesters_for_user(user)
        for semester in semesters:
            models.semester.clear_courses(semester['id'])
