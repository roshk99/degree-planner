"""
Useful functions for evaluating if requirements, prerequisites, or corequisites are met
"""

import re
import models.requirement
import models.course
import models.requisite
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


def evaluate_requisites(courses):
    """
    :param courses: should be a dictionary of length SEMESTER_NUM, where its elements are a list of courses
        (dictionary format) in that semester
    """
    master_dict = {}  # Should have the course id mapped to the semester taken
    for i in range(SEMESTER_NUM):
        semester = courses[i]
        for course in semester:
            master_dict[course['id']] = i

    messages = []
    missing_courses = []
    for course_id, semester_num in master_dict.items():
        requisites = models.requisite.get_requisites_for_course(course_id)
        for requisite in requisites:
            met = False
            course_options = requisite['requisites']
            for course in course_options:
                if course in master_dict:
                    if requisite['type'] == 'pre' and master_dict[course] < semester_num:
                        met = True
                    elif requisite['type'] == 'co' and master_dict[course] == semester_num:
                        met = True
            if not met and requisite['type'] == 'pre':
                my_course = models.course.get_course(course_id).to_json()
                messages.append(my_course['subject_code'] + ' ' + my_course['number'] + ' is missing prerequisites')
                for course_option_id in course_options:
                    missing_courses.append(models.course.get_course(course_option_id).to_json())
            if not met and requisite['type'] == 'co':
                my_course = models.course.get_course(course_id).to_json()
                messages.append(my_course['subject_code'] + ' ' + my_course['number'] + ' is missing corequisites')
                for course_option_id in course_options:
                    missing_courses.append(models.course.get_course(course_option_id).to_json())

    return messages, missing_courses
