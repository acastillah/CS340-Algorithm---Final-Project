from ..algorithm import *

def overflow_fill_classroom(teacher, course, classroomSize, timeslot, ds, schedule):
    studentsInClass = []
    availableStudents = ds["PossibleStudents"][course] - ds["StudentsInTimeslot"][timeslot]
    ds["PossibleStudents"][course] = ds["StudentsInTimeslot"][timeslot] & ds["PossibleStudents"][course]
    while classroomSize > 0 and availableStudents:
        student = availableStudents.pop()
        studentsInClass.append(student)
        ds["StudentsInTimeslot"][timeslot].add(student)
        classroomSize -= 1
    if teacher in ds["TeacherBusy"]:
        ds["TeacherBusy"][teacher].add(timeslot)
    else:
        ds["TeacherBusy"][teacher] = set([timeslot])
    ds["PossibleStudents"][course] = ds["PossibleStudents"][course] | availableStudents
    if (len(ds["TeacherBusy"][teacher]) < 3):
        if (len(ds["PossibleStudents"][course])/len(studentsInClass) > .2 and len(availableStudents) > 5):
            section_added = assign_class(ds, fill_classroom, schedule, course, True)
            ds = section_added[0]
            schedule = section_added[1]
    return (studentsInClass, ds)

def registrars(ds):
    initialize = initialize_schedule(ds, overflow_fill_classroom)
    schedule = initialize[0]
    ds = initialize[1]
    schedule = fill_schedule(ds, schedule, overflow_fill_classroom)
    return schedule
