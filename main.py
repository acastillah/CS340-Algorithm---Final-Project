import argparse, operator

parser = argparse.ArgumentParser(description="Test your algortihm for the registrar's problem!")
parser.add_argument('class_txt')
parser.add_argument('student_txt')
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

# returns a list of most popular classes
def get_popular_classes():
    possible_students = get_possible_students()
    popular_classes = []
    # Since dictionaries can't be sorted, create a list of
    # tuples (class, number of students interested)
    for course, student_list in possible_students.iteritems():
        popular_classes.append((course, len(student_list)))
    # Now sort in descending order
    popular_classes = sorted(popular_classes, key=lambda x: x[1], reverse=True)
    return popular_classes

