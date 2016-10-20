import argparse

parser = argparse.ArgumentParser(description="Test your algortihm for the registrar's problem!")
parser.add_argument('class_info')
parser.add_argument('student_prefs')
parser.add_argument('schedule')
args = parser.parse_args()


def extract_info(class_info, student_prefs, schedule):
    print open_this(class_info)
    print open_this(student_prefs)
    print open_this(schedule)
    return

def open_this(txt):
    with open('basic_project_files/'+txt, 'r') as text:
        read_data = text.read()
        return read_data

extract_info(args.class_info, args.student_prefs, args.schedule)
