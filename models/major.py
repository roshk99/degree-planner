"""
Model definition and functions for requirement.
"""

from google.appengine.ext import db


class Major(db.Model):
    name = db.StringProperty(required=True)
    requirements = db.StringProperty(required=True)
    university = db.StringProperty(required=True)

    def to_json(self):
        return {'name': self.name, 'requirements': self.requirements, 'id': str(self.key()),
                'university': self.university}

    def get_id(self):
        return str(self.key())

    def get_name(self):
        return self.name

    def get_requirements(self):
        return self.requirements

    def get_university(self):
        return self.university


def get_major(key):
    return Major.get(key)


def get_majors_for_university(university_id):
    result = []
    query = Major.gql('WHERE university = :1', university_id)
    for major in query:
        result.append(major.to_json())
    return result


def create_major(major, university_id):
    existing = get_majors_for_university(university_id)
    name_list = []
    for existing_major in name_list:
        name_list.append(existing_major['name'])

    if major['name'] not in name_list or not existing:
        major = Major(
            name=major['name'],
            requirements=major['requirements'],
            university=major['university']
        )
        major.put()
        return major
    else:
        return None


def delete_major(major):
    major.delete()
