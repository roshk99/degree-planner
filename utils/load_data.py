import models.requisite
import models.course
import models.major
import models.requirement
import models.university

import utils

import logging
import csv
import os


def load_data():

    # First get all the universities
    with open('./data/universities.csv') as csv_file:
        rows = csv.reader(csv_file)
        for row in rows:
            university_name = row[0]
            university = models.university.get_university_by_name(university_name)
            if not university:
                models.university.create_university({'name': university_name})

    # Now iterate through the folders in the universities folder
    root_dir = './data/universities'
    for subdir, dirs, files in os.walk(root_dir):
        for my_dir in dirs:
            if my_dir != 'requirements':

                # Check that we have the universities for the directories
                university = models.university.get_university_by_name(my_dir)
                if not university:
                    logging.info('The directory %s was not in the universities.csv file', my_dir)
                    return

                # For each university
                requisites = {}
                my_path = os.path.join(root_dir, my_dir)
                for dir_subdir, dir_dirs, dir_files in os.walk(my_path):
                    for file_name in dir_files:
                        if file_name == 'courses.csv':
                            with open(os.path.join(my_path, file_name)) as csv_file:
                                rows = csv.reader(csv_file)
                                for row in rows:
                                    name = row[0]
                                    description = row[1]
                                    number = row[2]
                                    subject_code = row[3]

                                    # Default value is 3
                                    if row[6] == '':
                                        credits_num = 3.0
                                    else:
                                        credits_num = float(row[6])

                                    if row[7] == '' or 'F/S':
                                        fall = True
                                        spring = True
                                    elif row[7] == 'F':
                                        fall = True
                                        spring = False
                                    elif row[7] == 'S':
                                        fall = False
                                        spring = True
                                    else:
                                        logging.info('Invalid fall/spring in %s that says %s',
                                                     os.path.join(my_path, file), row[7])
                                        fall = True
                                        spring = False

                                    # Update the course
                                    course = models.course.update_course({'name': name, 'description': description,
                                                                          'number': number,
                                                                          'subject_code': subject_code,
                                                                          'credits': credits_num, 'fall': fall,
                                                                          'spring': spring,
                                                                          'university': university['id']})

                                    # Store the requisites for later
                                    prerequisites = row[4]
                                    corequisites = row[5]
                                    requisites[course['id']] = {'pre': prerequisites, 'co': corequisites}
                logging.info('Processing requisites for university %s', university['name'])
                process_requisites(requisites, university['id'])
                logging.info('Finished requisites for university %s', university['name'])

    # Now find the requirements
    for subdir, dirs, files in os.walk(root_dir):
        for my_dir in dirs:
            if my_dir != 'requirements':
                # For each university
                university_name = my_dir
                university = models.university.get_university_by_name(university_name)

                my_path = os.path.join(root_dir, my_dir)
                for dir_subdir, dir_dirs, dir_files in os.walk(my_path):
                    for file_name in dir_files:
                        if file_name != 'courses.csv':
                            major_name = file_name.split('.')[0]

                            # Create the major if it doesn't exist, if it does, delete all current requirements
                            major = models.major.get_major_by_name(major_name, university['id'])
                            if not major:
                                major = models.major.create_major({'name': major_name}, university['id'])
                            else:
                                models.requirement.delete_requirements_for_major(major['id'])

                            # Now add the requirements
                            with open(os.path.join(my_path, 'requirements', file_name)) as csv_file:
                                rows = csv.reader(csv_file)
                                for row in rows:
                                    add_requirement(row, major['id'], university['id'])
                            logging.info('Finished updating requirements for university %s and major %s',
                                         university['name'], major['name'])


def process_requisites(requisites, university_id):
    for course_id, requisite_dict in requisites.items():
        # First delete all requisites for the current course
        models.requisite.delete_requisites_for_course(course_id)

        # Now add all the new requisites
        prereq_str = requisite_dict['pre']
        coreq_str = requisite_dict['co']
        if prereq_str != '':
            utils.parse_requisite_str(course_id, 'pre', prereq_str, university_id)
        if coreq_str != '':
            utils.parse_requisite_str(course_id, 'co', coreq_str, university_id)


def add_requirement(row, major_id, university_id):
    number = int(row[0])
    courses = []
    for i in range(1, len(row)):
        course_str = row[i]
        if course_str != '':
            subject_code, course_number = course_str.split(' ')
            course = models.course.find_course(subject_code, course_number, university_id)
            if not course:
                logging.info('Could not find the course %s %s with university id %s', subject_code,
                             course_number, university_id)
                return
            else:
                courses.append(course['id'])
    models.requirement.create_requirement({'number': number, 'courses': courses}, major_id)
