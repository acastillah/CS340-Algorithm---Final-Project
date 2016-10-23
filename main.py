import argparse
from generate_data_structures import *

parser = argparse.ArgumentParser(description="Test your algortihm for the registrar's problem!")
parser.add_argument('constraints_txt')
parser.add_argument('students_txt')
parser.add_argument('schedule_txt')

args = parser.parse_args()


# return a list of lists
def extract_info(txt):
    text = iter(open('basic_project_files/'+txt, 'r'))
    next(text) # Skip the first line
    results = []
    for line in text:
        line = line.strip()
        results.append(line.split())
    text.close()
    return results

student_preferences = extract_info(args.students_txt)
constraints = extract_info(args.constraints_txt)

# ADTs = generate(student_preferences, constraints) # this generates all data structures
# schedule = registrars(ADTs)                       # returns the schedule which we will write 



