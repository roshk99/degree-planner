"""
Model definition and functions for user.
"""

from google.appengine.ext import db
import uuid
import hashlib


class User(db.Model):
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    university = db.StringProperty(required=True)
    majors = db.ListProperty(str)

    def to_json(self):
        return {'first_name': self.first_name, 'last_name': self.last_name, 'id': str(self.key()), 'email': self.email,
                'password': self.password, 'university': self.university, 'majors': self.majors}

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

    def set_university(self, university):
        self.university = university

    def set_majors(self, majors):
        self.majors = majors

    def clear_majors(self):
        self.majors = []


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

    salt = uuid.uuid4().hex

    if user['email'] not in name_list or not existing:
        user = User(
            first_name=user['first_name'],
            last_name=user['last_name'],
            email=user['email'],
            password=hashlib.sha256(salt.encode() + user['password'].encode()).hexdigest() + ':' + salt,
            university=user['university'])
        user.put()
        return user.to_json()
    else:
        return None


def check_user(data):
    query = User.gql('WHERE email=:1', data['email'])
    if query.count() == 0:
        return None

    for user in query:
        found_user = user
        hashed_password = found_user.get_password()
    password, salt = hashed_password.split(':')
    user_password = data['password']

    if password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest():
        return found_user.to_json()
    else:
        return None


def add_major(user, major_id):
    majors = user.get_majors()
    print 'majors', majors
    print 'major_id', major_id
    if major_id in majors:
        return None
    else:
        if len(majors) == 0:
            user.set_majors([major_id])
        else:
            user.set_majors(majors.append(major_id))
        user.put()
        return major_id


def clear_majors(user):
    user.clear_majors()
    user.put()


def delete_user(user):
    user.delete()
