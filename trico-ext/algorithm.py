from ..algorithm import *

def onCampus(student, timeslot, school, ds):
    previous_ts = timeslot - 1
    next_ts = timeslot + 1
    if student in ds["CourseInTimeslot"]:
        if previous_ts in ds["CourseInTimeslot"][student]:
            previous_course = ds["CourseInTimeslot"][student][previous_ts]
            if school != ds["SchoolOfCourse"][previous_course]:
                print "Not on campus"
                return False
        if next_ts in ds["CourseInTimeslot"][student]:
            next_course = ds["CourseInTimeslot"][student][next_ts]
            if school != ds["SchoolOfCourse"][next_course]:
                return False
    return True

def bico_fill_classroom(teacher, course, classroomSize, timeslot, ds, schedule):
    studentsInClass = []
    availableStudents = ds["PossibleStudents"][course] - ds["StudentsInTimeslot"][timeslot]
    school = ds["SchoolOfCourse"][course]
    while classroomSize > 0 and availableStudents:
        student = availableStudents.pop()
        if onCampus(student, timeslot, school, ds):
            studentsInClass.append(student)
            ds["StudentsInTimeslot"][timeslot].add(student)
            if student in ds["CourseInTimeslot"]:
                ds["CourseInTimeslot"][student][timeslot] = course
            else:
                ds["CourseInTimeslot"][student] = {}
                ds["CourseInTimeslot"][student][timeslot] = course
            classroomSize -= 1
    ds["PossibleStudents"][course] = availableStudents | ds["StudentsInTimeslot"][timeslot]
    if teacher in ds["TeacherBusy"]:
        ds["TeacherBusy"][teacher].add(timeslot)
    else:
        ds["TeacherBusy"][teacher] = set([timeslot])
    return (studentsInClass, ds, schedule)

def get_optimal_bico_ts(timeslotsTeacherFree, ds, course):
    metric = float("-inf")
    optimalMetric = float("-inf")
    optimalTimeslot = None
    school = ds["SchoolOfCourse"][course]
    #figuring out the best timeslot to assign students and class to
    for timeslot in timeslotsTeacherFree:
        classroom = ds["PossibleClassrooms"][timeslot][0][0] #classroom id
        numOfAvailableStudents = 0
        for student in ds["PossibleStudents"][course]:
            if onCampus(student, timeslot, school, ds) and student not in ds["StudentsInTimeslot"][timeslot]:
                numOfAvailableStudents += 1
        classroomSize = ds["ClassroomSize"][classroom]
        if classroomSize > numOfAvailableStudents:
            metric = numOfAvailableStudents
        else:
            metric = classroomSize
        if metric > optimalMetric:
            optimalTimeslot = timeslot
            optimalMetric = metric
    return (optimalMetric, optimalTimeslot)

def registrars(ds):
    initialize = initialize_schedule(ds, bico_fill_classroom)
    schedule = initialize[0]
    ds = initialize[1]
    schedule = fill_schedule(ds, schedule, bico_fill_classroom, get_optimal_bico_ts)
    return schedule
