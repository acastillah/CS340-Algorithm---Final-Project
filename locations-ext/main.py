
from generate_data_structures_locations import *
from ..main import *
from algorithm import *
import argparse
import os

parser = argparse.ArgumentParser('Multiple sections extension')
parser.add_argument('constraints')
parser.add_argument('students')
parser.add_argument('schedule')

args = parser.parse_args()

constraints_txt = args.constraints
students_txt = args.students
schedule_txt = args.schedule

student_preferences = extract_info(students_txt)
constraints = extract_info(constraints_txt)

ADTs = generate(student_preferences, constraints) # this generates all data structures
schedule = registrars(ADTs)                       # returns the schedule which we will write

write_info(schedule, schedule_txt)


# subprocess.call(['perl', 'cs340_project/sections-ext/is_valid.pl', constraints_txt, students_txt, schedule_txt])
