from collections import namedtuple
PopularClass = namedtuple('PopularClass', 'id students size')
Student = namedtuple('Student', 'id year major')

import argparse

parser = argparse.ArgumentParser(description="Test your algortihm for the registrar's problem!")
parser.add_argument('constraints_txt')
parser.add_argument('students_txt')

args = parser.parse_args()

# open(args.constraints_txt, 'w').close()
# open(args.students_txt, 'w').close()


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


# print student_preferences
# print constraints

# returns a dict { class_number:course_number }
def generate_class_course(constraints):
    result = {}
    for line in constraints:
        if line[0] == 'Classes':
            number_of_classes = line[1]
            begin_point = constraints.index(line) + 1 # This is the part of text that marks the beginning of the list of classes
        elif line[0] == 'Teachers':
            end_point = constraints.index(line)
            
    for course in constraints[begin_point:end_point]:
    	# course[0] = class id
    	# course[1] = course id
		result[course[0]] = course[1]
		
    return result
    
# returns a dictionary {Class: { set of student_objects that want to take Class }}
def get_possible_students(student_preference_list):
    possible_students = {}
    for student in student_preference_list:
        student_object = Student(id=student[0], year=student[1], major=student[2])
        student = iter(student)
        next(student) # skip student ID
        next(student) # skip student year
        next(student) # skip student major
        for class_preference in student:
            if class_preference in possible_students:
                possible_students[class_preference].add(student_object)
            else:
                possible_students[class_preference] = set([student_object])
    return possible_students

# print generate_class_course(constraints)
print get_possible_students(student_preferences)