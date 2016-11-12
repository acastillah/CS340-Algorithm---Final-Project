from ..algorithm import *

def overflow_fill_classroom(teacher, course, classroomSize, availableStudents, timeslot, ds,schedule):
    studentsInClass = []
    while classroomSize > 0 and availableStudents:
        student = availableStudents.pop()
        studentsInClass.append(student)
        ds["StudentsInTimeslot"][timeslot].add(student)
        classroomSize -= 1
    if teacher in ds["TeacherBusy"]:
        ds["TeacherBusy"][teacher].add(timeslot)
    else:
        ds["TeacherBusy"][teacher] = set([timeslot])
    if (len(ds["TeacherBusy"][teacher]) < 3):
        if (len(availableStudents)/len(studentsInClass) > .2 and len(availableStudents) > 5):
            print ("new section being made")
            section_added = assign_class(ds, fill_classroom, schedule, course, True)
            ds = section_added[0]
            schedule = section_added[1]
    return (studentsInClass, ds)

def multiple_sections(ds):
    initialize = initialize_schedule(ds, overflow_fill_classroom)
    schedule = initialize[0]
    ds = initialize[1]
    schedule = fill_schedule(ds, schedule, overflow_fill_classroom)
    return schedule
