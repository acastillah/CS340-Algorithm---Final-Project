from generate_data_structures import *
from algorithm import *
import subprocess
import argparse


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

def write_info(schedule):
    with open(schedule_txt, 'w') as finalized:
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test your algortihm for the registrar's problem!")
    
    parser.add_argument('-mode')
    
    args = parser.parse_args()
    
    if args.mode:
        print args.mode
    
    constraints_txt = input("Enter a name for your constraints file (please add quotes '<file>'): ")
    students_txt = input("Enter a name for your student preference file (please add quotes '<file>'): ")
    schedule_txt = input("Enter a name for your schedule file (output) (please add quotes '<file>'): ")
    
    print 

    open(constraints_txt, 'w').close()
    open(students_txt, 'w').close()

    room_num = str(input("Enter the number of rooms: "))
    class_num = str(input("Enter the number of classes: "))
    times_num = str(input("Enter the number of timeslots: "))
    students_num = str(input("Enter the number of students: "))
    
    if args.mode == "base": 
        subprocess.call(['perl', 'make_random_input.pl', room_num, class_num, times_num, students_num, constraints_txt, students_txt])

    ext_dir = args.mode+"-ext/"
    ext_randr = ext_dir+"make_random_input.pl"

    elif args.mode == "seniority":
        majors_num = str(input("Enter the number of distinct majors: "))
        subprocess.call(['perl', ext_randr, room_num, class_num, times_num, students_num, constraints_txt, students_txt, majors_num])
    elif args.mode == "locations":
        building_num = str(input("Enter the number of buildings: "))
        subprocess.call(['perl', ext_randr, room_num, class_num, times_num, students_num, constraints_txt, students_txt, building_num])
    elif args.mode == "sections":
        subprocess.call(['perl', ext_randr, roon_num, class_num, times_num, students_num, constraints_txt, students_txt]) 


    if args.mode = "base":
        student_preferences = extract_info(students_txt)
        constraints = extract_info(constraints_txt)

        ADTs = generate(student_preferences, constraints) # this generates all data structures
        schedule = registrars(ADTs)                       # returns the schedule which we will write

        write_info(schedule)
        subprocess.call(['perl', 'is_valid.pl', constraints_txt, students_txt, schedule_txt])

    else:
        subprocess.call(['python', ext_dir+'main.py'])

