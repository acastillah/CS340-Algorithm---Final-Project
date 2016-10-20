import argparse

parser = argparse.ArgumentParser(description="Test your algortihm for the registrar's problem!")
parser.add_argument('class_info')
parser.add_argument('student_prefs')
parser.add_argument('schedule')

args = parser.parse_args()


def extend_info(class_info, student_prefs):
    class_info = open_this(class_info)
    student_prefs = open_this(student_prefs)
    return

def open_this(txt):
    with open('basic_project_files/'+txt, 'r') as text:
        read_data = text.read()
        return read_data

extend_info(args.class_info, args.student_prefs)
# write_schedule(args.schedule)
