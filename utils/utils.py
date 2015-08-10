import models.requisite
import models.course


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
