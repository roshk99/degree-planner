"""
Model definition and functions for university.
"""

from google.appengine.ext import db


class University(db.Model):
    name = db.StringProperty(required=True)

    def to_json(self):
        return {'name': self.name, 'id': str(self.key())}

    def get_id(self):
        return str(self.key())

    def get_name(self):
        return self.name


def get_university(key):
    return University.get(key)


def get_all_universities():
    result = []
    query = University.gql('')
    for university in query:
        result.append(university.to_json())
    return result


def create_university(university):
    existing = get_all_universities()
    name_list = []
    for existing_university in existing:
        name_list.append(existing_university['name'])

    if university['name'] not in name_list or not existing:
        university = University(
            name=university['name']
        )
        university.put()
        return university
    else:
        return None


def delete_university(university):
    university.delete()
