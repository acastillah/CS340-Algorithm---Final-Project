import argparse

parser = argparse.ArgumentParser(description="Test your algortihm for the registrar's problem!")
parser.add_argument('class_info')
parser.add_argument('student_prefs')
parser.add_argument('schedule')
args = parser.parse_args()


def extract_info(class_info, student_prefs, schedule):
    print class_info
    print student_prefs
    print schedule
    return

extract_info(args.class_info, args.student_prefs, args.schedule)
