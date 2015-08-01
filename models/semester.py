"""
Model definition and functions for semester.
"""

from google.appengine.ext import db
from user import User


class Semester(db.Model):
    user = db.ReferenceProperty(User, required=True)
    number = db.IntegerProperty(required=True)
    courses = db.ListProperty(str)

    def to_json(self):
        return {'user': self.user.get_id(), 'number': self.number, 'id': str(self.key()), 'courses': self.courses}

    def get_id(self):
        return str(self.key())

    def get_user(self):
        return self.user

    def get_number(self):
        return self.number

    def get_courses(self):
        return self.courses

    def set_courses(self, courses):
        self.courses = courses


def get_semester(key):
    return Semester.get(key)


def get_semesters_for_user(user):
    result = []
    query = Semester.gql('WHERE user = :1', user)
    for semester in query:
        result.append(semester.to_json())
    return result


def create_semester(user, semester):
    existing = get_semesters_for_user(user)
    name_list = []
    for existing_semester in existing:
        name_list.append(existing_semester['number'])

    if semester['number'] not in name_list or not existing:
        semester = Semester(
            user=user,
            number=semester['number'],
            courses=semester['courses']
        )
        semester.put()
        return semester
    else:
        return None


def delete_semester(semester):
    semester.delete()


def update_classes(semester_id, courses):
    semester = get_semester(semester_id)
    semester.set_courses(courses)
    semester.put()
    return


def clear_classes(semester_id):
    semester = get_semester(semester_id)
    semester.set_courses([])
    semester.put()
    return
