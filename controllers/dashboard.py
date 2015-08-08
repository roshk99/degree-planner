import webapp2
import pages
import authentication.auth
import csv

from config import *

import models.user
import models.semester
import models.course
import models.university
import models.major
import models.requirement


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # with open('./data/universities.csv', 'r') as csvfile:
        #     spamreader = csv.reader(csvfile)
        #     for row in spamreader:
        #         print row
        #         print ', '.join(row)

        user = authentication.auth.get_logged_in_user()
        if not user:
            self.redirect(ERROR_URI)

        university = models.university.get_university(user.get_university()).to_json()
        semesters = models.semester.get_semesters_for_user(user)

        all_courses = {}
        for semester in semesters:
            courses = []
            for course_id in semester['courses']:
                courses.append(models.course.get_course(course_id).to_json())
            all_courses[int(semester['number'])] = courses

        my_university = university['name']
        my_majors = models.major.get_majors_for_university(university['id'])

        view = pages.render_view(DASHBOARD_URI, {'first_name': user.get_first_name(),
                                                 'last_name': user.get_last_name(),
                                                 'email': user.get_email(),
                                                 'my_university': my_university,
                                                 'my_majors': my_majors,
                                                 'my_courses': all_courses,
                                                 'universities': models.university.get_all_universities()})
        pages.render_page(self, view)
