import pages
import webapp2
import authentication.auth
import logging
import json

from config import *

import models.user
import models.semester
import models.course
import models.university
import models.major
import models.requirement
import models.requisite
import utils.rules
import utils.utils


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = authentication.auth.get_logged_in_user()
        if not user:
            authentication.auth.redirect_to_login(self)

        semesters = models.semester.get_semesters_for_user(user)
        my_courses = {}
        all_my_courses = []
        for semester in semesters:
            courses = []
            for course_id in semester['courses']:
                course = models.course.get_course(course_id).to_json()
                course = utils.utils.requisites_as_text(course)
                courses.append(course)
            all_my_courses.extend(courses)
            my_courses[int(semester['number'])] = courses
        majors = user.get_majors()
        logging.info("My Courses: %s", len(all_my_courses))

        requirements = []
        for major_id in majors:
            requirements.extend(models.requirement.get_requirements_for_major(major_id))

        requirements_eval = utils.rules.evaluate_requirements(my_courses, requirements)

        all_courses = []
        course_master = []
        for requirement in requirements_eval['not_met']:
            courses = []
            for course_id in requirement['courses']:
                course = models.course.get_course(course_id).to_json()
                course = utils.utils.requisites_as_text(course)
                if course not in course_master:
                    course_master.append(course)
                    courses.append(course)
            all_courses.append({'number': requirement['number'], 'courses': courses})

        messages, requisite_courses = utils.rules.evaluate_requisites(my_courses)

        missing_courses = []
        for requisite_course in requisite_courses:
            if requisite_course not in course_master:
                missing_courses.append(requisite_course)

        if len(missing_courses) > 0:
            all_courses.append({'number': 'requisites', 'courses': missing_courses})
        logging.info('All courses: %s', len(course_master) + len(missing_courses))

        view = pages.render_view(PLAN_URI, {'semester_num': SEMESTER_NUM,
                                            'my_courses': my_courses,
                                            'all_courses': all_courses,
                                            'messages': messages})
        pages.render_page(self, view)

    def post(self):
        user = authentication.auth.get_logged_in_user()
        if not user:
            authentication.auth.redirect_to_login(self)

        data = json.loads(self.request.get('data'))
        logging.info('Save Classes Post: %s', data)

        semesters = models.semester.get_semesters_for_user(user)
        for semester in semesters:
            semester_number = str(semester['number'])
            courses = data[semester_number]
            models.semester.update_courses(semester['id'], courses)

        self.response.out.write('Success')
