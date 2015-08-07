"""
Useful functions for evaluating if requirements, prerequisites, or corequisites are met
"""

import re
import models.requirement
import models.course


def evaluate_requirements(courses, requirements):
    """
    :param courses: should be a list of length SEMESTER_NUM, where its elements are a list of courses
        (dictionary format) in that semester
    :param requirements: should be a list of requirements in dictionary format
    """

    met_requirements = []
    not_met_requirements = []

    course_master = []
    for semester in courses:
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
            if course in course_master and not int(course['number']):
                num += 1
            # Special case if class format is like 3XX
            else:
                num_str = str(course['number'])
                match_str = num_str[0] + '..'
                for my_course in course_master:
                    if re.match(match_str, str(my_course['number'])):
                        num += 1

        if num >= number:
            met_requirements.append(requirement)
        else:
            not_met_requirements.append(requirement)

    return {'met': met_requirements, 'not_met': not_met_requirements}


def evaluate_prerequisites(courses):
    """
    :param courses: should be a list of length SEMESTER_NUM, where its elements are a list of courses
        (dictionary format) in that semester
    """
    prereqs = []
    for semester in courses:
        for course in semester:
            for prereq_id in course['prerequisites']:
                prereq = models.course.get_course(prereq_id).to_json()
                prereqs.append({'semester': semester['number'], 'course': course, 'prereq': prereq})

    unmet_prereqs = []
    for prereq_dict in prereqs:
        prereq = prereq_dict['prereq']
        course_semester = prereq_dict['semester']
        for semester in courses:
            if prereq in semester:
                num = semester['number']
        if num >= course_semester or not num:
            unmet_prereqs.append(course)

    return unmet_prereqs
