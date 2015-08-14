import models.requisite
import models.course
import models.major
import models.requirement
import models.university

import re
import logging

def requisites_as_text(course):
    requisites = models.requisite.get_requisites_for_course(course['id'])
    prereqs = []
    coreqs = []

    for requisite in requisites:
        course_options = []
        for course_id in requisite['requisites']:
            course_option = models.course.get_course(course_id).to_json()
            course_options.append(course_option['subject_code'] + ' ' + course_option['number'])
        if requisite['type'] == 'pre':
            prereqs.append(' OR '.join(course_options))
        else:
            coreqs.append(' OR '.join(course_options))

    prereqs = ', '.join(prereqs)
    coreqs = ', '.join(coreqs)

    course['prerequisites'] = prereqs
    course['corequisites'] = coreqs
    return course


def semester_as_list(semester):
    semester_list = []
    for course_id in semester:
        course = models.course.get_course(course_id).to_json()
        semester_list.append(course['subject_code'] + ' ' + str(course['number']) + ' - ' + str(course['credits']))
    return semester_list


def majors_as_text(majors_list):
    majors_text = []
    for major_id in majors_list:
        major = models.major.get_major(major_id).to_json()
        majors_text.append(major['name'])
    majors_text = ', '.join(majors_text)
    return majors_text


def add_test_data():
    university = models.university.create_university({'name': 'Rice University'})
    if not university:
        return
    university = university.to_json()
    major = models.major.create_major({'name': 'Mechanical Engineering'}, university['id']).to_json()
    course1 = models.course.create_course({'name': 'Introductory Calculus', 'credits': 3.0,
                                           'description': 'Calculus Class description', 'fall': False, 'spring': True,
                                           'number': '101', 'subject_code': 'MATH', 'university': university['id']}).to_json()
    course2 = models.course.create_course({'name': 'Introductory Chemistry', 'credits': 3.0,
                                       'description': 'Chemistry class description', 'fall': True, 'spring': True,
                                       'number': '200', 'subject_code': 'CHEM', 'university': university['id']}).to_json()
    course3 = models.course.create_course({'name': 'Statics Cource', 'credits': 3.0,
                                       'description': 'Statics class description', 'fall': True, 'spring': False,
                                       'number': '211', 'subject_code': 'MECH', 'university': university['id']}).to_json()
    course4 = models.course.create_course({'name': 'Another Chemistry Cource', 'credits': 3.0,
                                   'description': 'Another Chemistry Course description', 'fall': True, 'spring': True,
                                   'number': '201', 'subject_code': 'CHEM', 'university': university['id']}).to_json()

    requirement1 = models.requirement.create_requirement({'number': 1, 'courses': [course1['id']]}, major['id']).to_json()
    requirement2 = models.requirement.create_requirement({'number': 1, 'courses': [course2['id'], course4['id']]}, major['id']).to_json()
    requirement2 = models.requirement.create_requirement({'number': 1, 'courses': [course3['id']]}, major['id']).to_json()

    requisite1 = models.requisite.create_requisite({'type': 'pre', 'requisites': [course1['id']]}, course3['id']).to_json()
    requisite2 = models.requisite.create_requisite({'type': 'co', 'requisites': [course2['id']]}, course3['id']).to_json()
    requisite3 = models.requisite.create_requisite({'type': 'co', 'requisites': [course3['id']]}, course2['id']).to_json()


def parse_requisite_str(course_id, my_type, req_str, university_id):
    groups = re.findall('\((.*?)\)', req_str)
    for group in groups:
        req_arr = []
        arr = group.split(', ')
        for course_name in arr:
            subject_code, number = course_name.split(' ')
            course = models.course.find_course(subject_code, number, university_id)
            if not course:
                logging.info('Could not find the course %s %s for university id %s', subject_code, number, university_id)
                return
            req_arr.append(course['id'])

        models.requisite.create_requisite({'type': my_type, 'requisites': req_arr}, course_id)

