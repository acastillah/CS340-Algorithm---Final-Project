from generate_data_structures import *
from algorithm import *
import subprocess
import argparse
import os
import re

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

def extract_info_constraints(txt):
    text = iter(open(txt, 'r'))
    results = []
    for line in text:
        line = line.strip()
        results.append(line.split())
    text.close()
    return results

def write_info(schedule, schedule_txt):
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


    if args.mode == "presentation":
        student_preferences = extract_info("presentation16_prefs.txt")
        constraints = extract_info("presentation16_constraints.txt")

        ADTs = generate(student_preferences, constraints) # this generates all data structures
        schedule = registrars(ADTs)                       # returns the schedule which we will write

        write_info(schedule, "o.txt")
        subprocess.call(['perl', 'is_valid.pl', "presentation16_constraints.txt", "presentation16_prefs.txt", "o.txt"])
        print 
 
    elif args.mode == "experiment":
        constraints_txt = "c.txt"
        students_txt = "s.txt"
        schedule_txt = "o.txt"
        room_num = "1000"
        class_num = "1200"
        times_num = "12"
        majors_num = "26"
        with open("results.txt", 'w') as results:
            results.write("base,locations,sections,bico,students\n")
            for i in xrange(40,100, 5):
                students_num = str(i**2)
                open(constraints_txt, 'w').close()
                open(students_txt, 'w').close()
                subprocess.call(['perl', 'make_random_input.pl', room_num, class_num, times_num, students_num, constraints_txt, students_txt])
                student_preferences = extract_info(students_txt)
                constraints = extract_info(constraints_txt)
                ADTs = generate(student_preferences, constraints) # this generates all data structures
                schedule = registrars(ADTs)                       # returns the schedule which we will write
                write_info(schedule, schedule_txt)
                subprocess.call(['perl', 'is_valid.pl', constraints_txt, students_txt, schedule_txt])
                out = subprocess.check_output(['perl', 'is_valid.pl', constraints_txt, students_txt, schedule_txt])
                match = re.search("\d+", out)
                base_score = str(match.group(0))
                open("locations-ext/"+constraints_txt, 'w').close()
                open("locations-ext/"+students_txt, 'w').close()
                os.chdir("locations-ext/")
                subprocess.call(['perl', 'make_random_input.pl', room_num, class_num, times_num, students_num, constraints_txt, students_txt, majors_num])
                os.chdir('../../')
                subprocess.call(['python', '-m', ('cs340_project.locations-ext.main'), 'cs340_project/locations-ext/'+constraints_txt, 'cs340_project/locations-ext/'+students_txt, 'cs340_project/locations-ext/'+schedule_txt])
                out = subprocess.check_output(['python', '-m', ('cs340_project.locations-ext.main'), 'cs340_project/locations-ext/'+constraints_txt, 'cs340_project/locations-ext/'+students_txt, 'cs340_project/locations-ext/'+schedule_txt])
                match = re.search("\d+", out)
                locations_score = str(match.group(0))
                os.chdir('cs340_project')
                open("sections-ext/"+constraints_txt, 'w').close()
                open("sections-ext/"+students_txt, 'w').close()
                os.chdir("sections-ext/")
                subprocess.call(['perl', 'make_random_input.pl', room_num, class_num, times_num, students_num, constraints_txt, students_txt]) 
                os.chdir('../../')
                subprocess.call(['python', '-m', ('cs340_project.sections-ext.main'), 'cs340_project/sections-ext/'+constraints_txt, 'cs340_project/sections-ext/'+students_txt, 'cs340_project/sections-ext/'+schedule_txt])
                out = subprocess.check_output(['python', '-m', ('cs340_project.sections-ext.main'), 'cs340_project/sections-ext/'+constraints_txt, 'cs340_project/sections-ext/'+students_txt, 'cs340_project/sections-ext/'+schedule_txt])
                match = re.search("\d+", out)
                sections_score = str(match.group(0))
                os.chdir('cs340_project')
                open("bico-ext/"+constraints_txt, 'w').close()
                open("bico-ext/"+students_txt, 'w').close()
                os.chdir("bico-ext/")
                subprocess.call(['perl', 'make_random_input.pl', room_num, class_num, times_num, students_num, constraints_txt, students_txt]) 
                os.chdir('../../')
                subprocess.call(['python', '-m', ('cs340_project.bico-ext.main'), 'cs340_project/bico-ext/'+constraints_txt, 'cs340_project/bico-ext/'+students_txt, 'cs340_project/bico-ext/'+schedule_txt])
                out = subprocess.check_output(['python', '-m', ('cs340_project.bico-ext.main'), 'cs340_project/bico-ext/'+constraints_txt, 'cs340_project/bico-ext/'+students_txt, 'cs340_project/bico-ext/'+schedule_txt])
                match = re.search("\d+", out)
                bico_score = str(match.group(0))
                results.write(base_score+'\t'+locations_score+'\t'+sections_score+'\t'+bico_score+'\t'+students_num+'\n')
                os.chdir('cs340_project')

    else:
        constraints_txt = str(input("Enter a name for your constraints file (please add quotes '<file>'): "))
        if constraints_txt == "1":
            constraints_txt = "c.txt"
        students_txt = str(input("Enter a name for your student preference file (please add quotes '<file>'): "))
        if students_txt == "1":
            students_txt = "s.txt"
        schedule_txt = str(input("Enter a name for your schedule file (output) (please add quotes '<file>'): "))
        if schedule_txt == "1":
            schedule_txt = "o.txt"
        
        print 


        room_num = str(input("Enter the number of rooms: "))
        class_num = str(input("Enter the number of classes: "))
        times_num = str(input("Enter the number of timeslots: "))
        students_num = str(input("Enter the number of students: "))
        
        ext_dir = args.mode+"-ext"
        ext_randr = ext_dir+"/make_random_input.pl"

        if args.mode == "base": 
            open(constraints_txt, 'w').close()
            open(students_txt, 'w').close()
            subprocess.call(['perl', 'make_random_input.pl', room_num, class_num, times_num, students_num, constraints_txt, students_txt])
        else:
            open(ext_dir+"/"+constraints_txt, 'w').close()
            open(ext_dir+"/"+students_txt, 'w').close()
            os.chdir(ext_dir)
        if args.mode == "seniority":
            majors_num = str(input("Enter the number of distinct majors: "))
            subprocess.call(['perl', 'make_random_input.pl', room_num, class_num, times_num, students_num, constraints_txt, students_txt, majors_num])
        elif args.mode == "locations":
            majors_num = str(input("Enter the number of distinct majors: "))
            subprocess.call(['perl', 'make_random_input.pl', room_num, class_num, times_num, students_num, constraints_txt, students_txt, majors_num])
        elif args.mode == "sections":
            subprocess.call(['perl', 'make_random_input.pl', room_num, class_num, times_num, students_num, constraints_txt, students_txt]) 

        elif args.mode == "bico":
            subprocess.call(['perl', 'make_random_input.pl', room_num, class_num, times_num, students_num, constraints_txt, students_txt]) 

        if args.mode == "base":
            student_preferences = extract_info(students_txt)
            constraints = extract_info(constraints_txt)

            ADTs = generate(student_preferences, constraints) # this generates all data structures
            schedule = registrars(ADTs)                       # returns the schedule which we will write

            write_info(schedule, schedule_txt)
            subprocess.call(['perl', 'is_valid.pl', constraints_txt, students_txt, schedule_txt])

        else:
            os.chdir('../../')
            subprocess.call(['python', '-m', ('cs340_project.'+ext_dir+'.main'), 'cs340_project/'+ext_dir+'/'+constraints_txt, 'cs340_project/'+ext_dir+'/'+students_txt, 'cs340_project/'+ext_dir+'/'+schedule_txt])

