import argparse

parser = argparse.ArgumentParser(description="Test your algortihm for the registrar's problem!")
parser.add_argument('class_txt')
parser.add_argument('student_txt')
parser.add_argument('schedule_txt')

args = parser.parse_args()


def extend_info(class_txt, student_txt):
    extract_info(class_txt)
    extract_info(student_txt)
    return

def extract_info(txt):
    text = open('basic_project_files/'+txt, 'r')
    for line in text:
        line = line.strip()
        print line
    text.close()

extend_info(args.class_txt, args.student_txt)
# write_schedule(args.schedule)
