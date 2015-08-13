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
    fall = db.BooleanProperty(required=True)
    spring = db.BooleanProperty(required=True)

    def to_json(self):
        return {'name': self.name, 'id': str(self.key()), 'description': self.description,
                'number': self.number, 'subject_code': self.subject_code, 'credits': self.credits,
                'university': self.university, 'fall': self.fall, 'spring': self.spring}

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

    def get_credits(self):
        return self.credits

    def get_university(self):
        return self.university

    def get_fall(self):
        return self.fall

    def get_spring(self):
        return self.spring


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
            credits=course['credits'],
            university=course['university'],
            fall=course['fall'],
            spring=course['spring']
        )
        course.put()
        return course
    else:
        return None


def update_course(course):
    result = create_course(course)
    if not result:
        # Update the existing course information
        query = Course.gql('WHERE subject_code = :1 AND number = :2 AND university = :3',
                           course['subject_code'], course['number'], course['university'])
        for my_course in query:
            my_course.name = course['name']
            my_course.description = course['description']
            my_course.credits = course['credits']
            my_course.fall = course['fall']
            my_course.spring = course['spring']
            my_course.put()
            return my_course.to_json()
    else:
        return result.to_json()


def find_course(subject_code, number, university_id):
    query = Course.gql('WHERE subject_code = :1 AND number = :2 AND university = :3',
                           subject_code, number, university_id)
    for course in query:
        return course.to_json()


def delete_course(course):
    course.delete()
