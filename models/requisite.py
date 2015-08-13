"""
Model definition and functions for requirement.
"""

from google.appengine.ext import db


class Requisite(db.Model):
    course = db.StringProperty(required=True)
    type = db.StringProperty(required=True)
    requisites = db.ListProperty(str, required=True)

    def to_json(self):
        return {'course': self.course, 'type': self.type, 'id': str(self.key()), 'requisites': self.requisites}

    def get_id(self):
        return str(self.key())

    def get_course(self):
        return self.course

    def get_type(self):
        return self.type

    def get_requisites(self):
        return self.requisites


def get_requisite(key):
    return Requisite.get(key)


def get_requisites_for_course(course_id):
    result = []
    query = Requisite.gql('WHERE course = :1', course_id)
    for requisite in query:
        result.append(requisite.to_json())
    return result


def create_requisite(requisite, course_id):
    existing = get_requisites_for_course(course_id)
    name_list = []
    for existing_requisite in existing:
        name_list.append((existing_requisite['type'], existing_requisite['requisites']))

    if (requisite['type'], requisite['requisites']) not in name_list or not existing:
        requisite = Requisite(
            course=course_id,
            type=requisite['type'],
            requisites=requisite['requisites']
        )
        requisite.put()

        return requisite
    else:
        return None


def delete_requisites_for_course(course_id):
    requisites = get_requisites_for_course(course_id)
    for req in requisites:
        requisite = get_requisite(req['id'])
        delete_requisite(requisite)


def delete_requisite(requisite):
    requisite.delete()
