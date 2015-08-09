"""
Useful functions for evaluating if requirements, prerequisites, or corequisites are met
"""

import re
import models.requirement
import models.course
from config import *


def evaluate_requirements(courses, requirements):
    """
    :param courses: should be a dictionary of length SEMESTER_NUM, where its elements are a list of courses
        (dictionary format) in that semester
    :param requirements: should be a list of requirements in dictionary format
    """

    met_requirements = []
    not_met_requirements = []

    course_master = []
    for i in range(SEMESTER_NUM):
        semester = courses[i]
        for course in semester:
            course_master.append({'number': course['number'], 'subject_code': course['subject_code']})

    for requirement in requirements:
        number = requirement['number']
        course_list = []
        for course_id in requirement['courses']:
            course = models.course.get_course(course_id).to_json()
            course_list.append({'number': course['number'], 'subject_code': course['subject_code']})

        num = 0
        for course in course_list:
            print course
            if int(course['number']):
                if course in course_master:
                    num += 1
            else:
                # Special case if class format is like 3XX or XXX
                num_str = str(course['number'])
                if int(num_str[0]):
                    match_str = num_str[0] + '..'
                else:
                    match_str = '...'
                for my_course in course_master:
                    if my_course['subject_code'] == course['subject_code']:
                        if re.match(match_str, str(my_course['number'])):
                            num += 1

        if num >= number:
            met_requirements.append(requirement)
        else:
            not_met_requirements.append(requirement)

    return {'met': met_requirements, 'not_met': not_met_requirements}


def evaluate_prerequisites(courses):
    """
    :param courses: should be a dictionary of length SEMESTER_NUM, where its elements are a list of courses
        (dictionary format) in that semester
    """

    prereqs = []
    for i in range(SEMESTER_NUM):
        semester = courses[i]
        for course in semester:
            for prereq in course['prerequisites']:
                prereqs.append({'semester': i, 'course': course, 'prereq': prereq})

    unmet_prereqs = []
    for prereq_dict in prereqs:
        prereq = prereq_dict['prereq']
        course = prereq_dict['course']
        course_semester = prereq_dict['semester']
        num = float('inf')
        for i in range(SEMESTER_NUM):
            semester = courses[i]
            for semester_course in semester:
                if prereq['id'] == semester_course['id']:
                    num = i
        if num >= course_semester:
            unmet_prereqs.append(course)

    return unmet_prereqs


def evaluate_corequisites(courses):
    """
    :param courses: should be a dictionary of length SEMESTER_NUM, where its elements are a list of courses
        (dictionary format) in that semester
    """

    coreqs = []
    for i in range(SEMESTER_NUM):
        semester = courses[i]
        for course in semester:
            for coreq in course['corequisites']:
                coreqs.append({'semester': i, 'course': course, 'coreq': coreq})

    unmet_coreqs = []
    for coreq_dict in coreqs:
        coreq = coreq_dict['coreq']
        print 'Coreq', coreq['name']
        course = coreq_dict['course']
        print 'Course', course['name']
        course_semester = coreq_dict['semester']
        num = float('inf')
        for i in range(SEMESTER_NUM):
            semester = courses[i]
            for semester_course in semester:
                if coreq['id'] == semester_course['id']:
                    num = i
        print 'Num', num
        if num != course_semester:
            unmet_coreqs.append(course)

    return unmet_coreqs
