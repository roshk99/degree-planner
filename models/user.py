"""
Model definition and functions for user.
"""

from google.appengine.ext import db


class User(db.Model):
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    university = db.StringProperty(required=True)
    majors = db.ListProperty(str, required=True)
    semesters = db.ListProperty(str, required=True)

    def to_json(self):
        return {'first_name': self.first_name, 'last_name': self.last_name, 'id': str(self.key()), 'email': self.email,
                'password': self.password, 'university': self.university, 'majors': self.majors,
                'semesters': self.semesters}

    def get_id(self):
        return str(self.key())

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def get_university(self):
        return self.university

    def get_majors(self):
        return self.majors

    def get_semesters(self):
        return self.semesters


def get_user(key):
    return User.get(key)


def get_all_users():
    result = []
    query = User.gql('')
    for user in query:
        result.append(user.to_json())
    return result


def create_user(user):
    existing = get_all_users()
    name_list = []
    for existing_users in existing:
        name_list.append(existing_users['email'])

    if user['email'] not in name_list or not existing:
        user = User(
            first_name=user['first_name'],
            last_name=user['last_name'],
            email=user['email'],
            password=user['password'],
            university=user['university'],
            majors=user['majors'],
            semesters=user['semesters'])
        user.put()
        return user
    else:
        return None


def delete_user(user):
    user.delete()
