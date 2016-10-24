from collections import namedtuple

def registrars(ds):
    ds["TeacherBusy"] = {}
    ds["StudentsInTimeslot"] = {}
    schedule = []
    for timeslot in ds["Timeslots"]:
        classroom = ds["PossibleClassrooms"][timeslot].pop(0)[0] # largest classroom available at timeslot
        course = ds["PopularClasses"].pop(0).id # Most popular class
        classroomSize = ds["ClassroomSize"][classroom]
        studentsInClass = []
        ds["StudentsInTimeslot"][timeslot] = set()
        while classroomSize > 0 and ds["PossibleStudents"][course]:
            student = ds["PossibleStudents"][course].pop()
            studentsInClass.append(student)
            ds["StudentsInTimeslot"][timeslot].add(student)
            classroomSize -= 1
        teacher = ds["ClassTeacher"][course]
        schedule.append((course, classroom, teacher, timeslot, studentsInClass))
        if teacher in ds["TeacherBusy"]:
            ds["TeacherBusy"][teacher].add(timeslot)
        else:
            ds["TeacherBusy"][teacher] = set([timeslot])
        if not ds["PossibleClassrooms"][timeslot]:
            ds["PossibleClassrooms"].pop(timeslot)
    while ds["PopularClasses"] and ds["PossibleClassrooms"]:
        course = ds["PopularClasses"].pop(0).id
        teacher = ds["ClassTeacher"][course]
        if teacher in ds["TeacherBusy"]:
            timeslotsTeacherFree = ds["Timeslots"] - ds["TeacherBusy"][teacher]
        else:
            timeslotsTeacherFree = ds["Timeslots"]
        metric = float("-inf")
        optimalMetric = float("-inf")
        optimalTimeslot = None
        #figuring out the best timeslot to assign students and class to
        for timeslot in timeslotsTeacherFree:
            classroom = ds["PossibleClassrooms"][timeslot][0][0] #classroom id
            numOfAvailableStudents = len(ds["PossibleStudents"][course] - ds["StudentsInTimeslot"][timeslot])
            classroomSize = ds["ClassroomSize"][classroom]
            if classroomSize > numOfAvailableStudents:
                metric = numOfAvailableStudents
            else:
                metric = classroomSize
            if metric > optimalMetric:
                optimalTimeslot = timeslot
                optimalMetric = metric
        if optimalMetric == 0:
            break
        classroom = ds["PossibleClassrooms"][optimalTimeslot].pop(0)[0] # largest classroom available at timeslot
        if not ds["PossibleClassrooms"][optimalTimeslot]:
            ds["PossibleClassrooms"].pop(optimalTimeslot)
        classroomSize = ds["ClassroomSize"][classroom]
        availableStudents = ds["PossibleStudents"][course] - ds["StudentsInTimeslot"][optimalTimeslot]
        studentsInClass = []
        while classroomSize > 0 and availableStudents:
            student = availableStudents.pop()
            studentsInClass.append(student)
            ds["StudentsInTimeslot"][optimalTimeslot].add(student)
            classroomSize -= 1
        teacher = ds["ClassTeacher"][course]
        schedule.append((course, classroom, teacher, timeslot, studentsInClass))
        if teacher in ds["TeacherBusy"]:
            ds["TeacherBusy"][teacher].add(timeslot)
        else:
            ds["TeacherBusy"][teacher] = set([timeslot])
    return schedule


