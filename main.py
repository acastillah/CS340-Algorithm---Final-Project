from generate_data_structures import *
from algorithm import *
import subprocess
import argparse

parser = argparse.ArgumentParser(description="Test your algortihm for the registrar's problem!")
parser.add_argument('constraints_txt')
parser.add_argument('students_txt')
parser.add_argument('schedule_txt')

args = parser.parse_args()

open(args.constraints_txt, 'w').close()
open(args.students_txt, 'w').close()

room_num = str(input("Enter the number of rooms: "))
class_num = str(input("Enter the number of classes: "))
times_num = str(input("Enter the number of timeslots: "))
students_num = str(input("Enter the number of students: "))

subprocess.call(['perl', 'make_random_input.pl', room_num, class_num, times_num, students_num, args.constraints_txt, args.students_txt])

# return a list of lists
def extract_info(txt):
    text = iter(open(txt, 'r'))
    next(text) # Skip the first line
    results = []
    for line in text:
        line = line.strip()
        results.append(line.split())
    text.close()
    return results

student_preferences = extract_info(args.students_txt)
constraints = extract_info(args.constraints_txt)

ADTs = generate(student_preferences, constraints) # this generates all data structures
schedule = registrars(ADTs)                       # returns the schedule which we will write 

def write_info(schedule):
    with open(args.schedule_txt, 'w') as finalized:
        finalized.write('Course\tRoom\tTeacher\tTime\tStudents\n')
        for course_info in schedule:
            for column in course_info:
                if column == course_info[-1]:
                    for student in column:
                        finalized.write(student+" ")
                else:
                    finalized.write(str(column))
                    finalized.write('\t')
            finalized.write('\n')

write_info(schedule)

subprocess.call(['perl', 'is_valid.pl', args.constraints_txt, args.students_txt, args.schedule_txt])
