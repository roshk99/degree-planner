import pages
import webapp2
import authentication.auth
import logging

from config import *

import models.user
import models.semester
import models.course
import models.university
import models.major
import models.requirement
import rules.rules


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = authentication.auth.get_logged_in_user()
        if not user:
            self.redirect(ERROR_URI)

        semesters = models.semester.get_semesters_for_user(user)
        my_courses = {}
        all_my_courses = []
        for semester in semesters:
            courses = []
            for course_id in semester['courses']:
                courses.append(models.course.get_course(course_id).to_json())
            all_my_courses.extend(courses)
            my_courses[int(semester['number'])] = courses
        majors = user.get_majors()
        logging.info("My Courses: %s", my_courses)

        requirements = []
        for major_id in majors:
            requirements.extend(models.requirement.get_requirements_for_major(major_id))

        requirements_eval = rules.rules.evaluate_requirements(my_courses, requirements)

        all_courses = []
        for requirement in requirements_eval['not_met']:
            courses = []
            for course_id in requirement['courses']:
                courses.append(models.course.get_course(course_id).to_json())
            all_courses.append(courses)
        logging.info('All courses: %s', all_courses)

        view = pages.render_view(PLAN_URI, {'semester_num': SEMESTER_NUM,
                                            'my_courses': my_courses,
                                            'all_courses': all_courses})
        pages.render_page(self, view)
