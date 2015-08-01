"""
Model definition and functions for course.
"""

from google.appengine.ext import db


class Course(db.Model):
    name = db.StringProperty(required=True)
    description = db.StringProperty()
    university = db.StringProperty(required=True)
    number = db.StringProperty(required=True)
    subject_code = db.StringProperty(required=True)
    prerequisites = db.ListProperty(str)
    corequisites = db.ListProperty(str)
    credits = db.FloatProperty(required=True)

    def to_json(self):
        return {'name': self.name, 'id': str(self.key()), 'description': self.description,
                'number': self.number, 'subject_code': self.subject_code, 'prerequisites': self.prerequisites,
                'corequisites': self.corequisites, 'credits': self.credits, 'university': self.university}

    def get_id(self):
        return str(self.key())

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_number(self):
        return self.number

    def get_subject_code(self):
        return self.subject_code

    def get_prerequisites(self):
        return self.prerequisites

    def get_corequisites(self):
        return self.corequisites

    def get_credits(self):
        return self.credits

    def get_university(self):
        return self.university


def get_course(key):
    return Course.get(key)


def get_all_courses():
    result = []
    query = Course.gql('')
    for course in query:
        result.append(course.to_json())
    return result


def create_course(course):
    existing = get_all_courses()
    name_list = []
    for existing_course in existing:
        name_list.append((existing_course['university'], existing_course['number'], existing_course['subject_code']))

    if (course['university'], course['number'], course['subject_code']) not in name_list or not existing:
        course = Course(
            name=course['name'],
            description=course['description'],
            number=course['number'],
            subject_code=course['subject_code'],
            prerequisites=course['prerequisites'],
            corequisites=course['corequisites'],
            credits=course['credits'],
            university=course['university']
        )
        course.put()
        return course
    else:
        return None


def delete_course(course):
    course.delete()
