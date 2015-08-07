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


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = authentication.auth.get_logged_in_user()
        if not user:
            self.redirect(ERROR_URI)

        university = models.university.get_university(user.get_university()).to_json()
        # # # university_id = user.get_university()
        # # # university = models.university.get_university(university_id)
        # course = models.course.create_course({'name': 'Statics', 'description': 'Statics description', 'number': '211', 'subject_code': 'MECH',
        #                 'prerequisites': [], 'corequisites': [], 'credits': 3.0, 'university': university['id'],
        #                 'fall': True, 'spring': True}).to_json()
        # major = models.major.create_major({'name': 'Mechanical Engineering'}, university['id']).to_json()
        # requirement = models.requirement.create_requirement({'number': 1, 'courses': [course['id']]}, major['id']).to_json()
        # semesters = models.semester.get_semesters_for_user(user.get_id())
        # for semester in semesters:
        #     if semester.to_json()['number'] == 0:
        #         semester.set_courses([course])
        # user.set_majors([major['id']])
        # # user.set_university(university['id'])
        # #user.set_university('ahJkZXZ-ZGVncmVlLXBsYW5uZXJyFwsSClVuaXZlcnNpdHkYgICAgIDAvwoM')

        # semesters = models.semester.get_semesters_for_user(user)
        # course = models.course.get_course('ahJkZXZ-ZGVncmVlLXBsYW5uZXJyEwsSBkNvdXJzZRiAgICAgKCkCQw').to_json()
        # for semester in semesters:
        #     if semester['number'] == 0:
        #         models.semester.update_courses(semester['id'], [course['id']])

        semesters = models.semester.get_semesters_for_user(user)
        all_courses = {}
        for semester in semesters:
            courses = []
            for course_id in semester['courses']:
                courses.append(models.course.get_course(course_id).to_json())
            print courses
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
