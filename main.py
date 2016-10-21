import argparse, operator

parser = argparse.ArgumentParser(description="Test your algortihm for the registrar's problem!")
parser.add_argument('class_txt')
parser.add_argument('student_txt')
parser.add_argument('schedule_txt')

args = parser.parse_args()


def extend_info(txt):
    return extract_info(txt)

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

# extend_info(args.student_txt)
# write_schedule(args.schedule)

# returns a dictionary {Class: {Students that want to take Class}
def get_possible_students():
    student_preference_list = extract_info(args.student_txt)
    possible_students = {}

    for student in student_preference_list:
        student_id = student[0]

        student = iter(student)
        next(student) # skip student ID
        for class_preference in student:
            if class_preference in possible_students:
                possible_students[class_preference].append(student_id)
            else:
                possible_students[class_preference] = [student_id]
    return possible_students

print get_possible_students()
