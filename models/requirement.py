"""
Model definition and functions for requirement.
"""

from google.appengine.ext import db


class Requirement(db.Model):
    number = db.IntegerProperty(required=True)
    courses = db.ListProperty(str, required=True)
    major = db.StringProperty(required=True)

    def to_json(self):
        return {'number': self.number, 'courses': self.courses, 'id': str(self.key()), 'major': self.major}

    def get_id(self):
        return str(self.key())

    def get_number(self):
        return self.number

    def get_courses(self):
        return self.courses

    def get_major(self):
        return self.major


def get_requirement(key):
    return Requirement.get(key)


def get_requirements_for_major(major_id):
    result = []
    query = Requirement.gql('WHERE major = :1', major_id)
    for requirement in query:
        result.append(requirement.to_json())
    return result


def create_requirement(requirement, major_id):
    existing = get_requirements_for_major(major_id)
    name_list = []
    for existing_requirement in existing:
        name_list.append((existing_requirement['number'], existing_requirement['courses']))

    if (requirement['number'], requirement['courses']) not in name_list or not existing:
        requirement = Requirement(
            number=requirement['number'],
            major=major_id,
            courses=requirement['courses']
        )
        requirement.put()
        return requirement
    else:
        return None


def delete_requirement(requirement):
    requirement.delete()
