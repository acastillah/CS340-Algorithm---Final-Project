#extensions: major/minor and class year priority, multiple sections, tri-co bus schedule, classrooms by location, diversity, overlapping timeslots

def fill_classroom(teacher, course, classroomSize, timeslot, ds, schedule, func_optimal_ts):
    studentsInClass = []
    availableStudents = ds["PossibleStudents"][course] - ds["StudentsInTimeslot"][timeslot]
    while classroomSize > 0 and availableStudents:
        student = availableStudents.pop()
        studentsInClass.append(student)
        ds["StudentsInTimeslot"][timeslot].add(student)
        classroomSize -= 1
    ds["PossibleStudents"][course] = availableStudents | ds["StudentsInTimeslot"][timeslot]
    if teacher in ds["TeacherBusy"]:
        ds["TeacherBusy"][teacher].add(timeslot)
    else:
        ds["TeacherBusy"][teacher] = set([timeslot])
    return (studentsInClass, ds, schedule)

def get_optimal_ts(timeslotsTeacherFree, ds, course):
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
    return (optimalMetric, optimalTimeslot)

def initialize_schedule(ds, func_fill_classroom, func_optimal_ts):
    schedule = []
    ds["CourseInTimeslot"] = {}
    ds["TeacherBusy"] = {}
    ds["StudentsInTimeslot"] = {}
    for timeslot in ds["Timeslots"]:
        ds["StudentsInTimeslot"][timeslot] = set()
    for timeslot in ds["Timeslots"]:
        course = ds["PopularClasses"].pop(0).id # Most popular class
        classroom = ds["PossibleClassrooms"][timeslot].pop(0)[0] # largest classroom available at timeslot
        classroomSize = ds["ClassroomSize"][classroom]
        studentsInClass = []
        teacher = ds["ClassTeacher"][course]
        pair = func_fill_classroom(teacher, course, classroomSize, timeslot, ds, schedule, func_optimal_ts)
        ds = pair[1]
        studentsInClass = pair[0]
        schedule.append((course, classroom, teacher, timeslot, studentsInClass))
        if not ds["PossibleClassrooms"][timeslot]:
            ds["PossibleClassrooms"].pop(timeslot)
    return (schedule, ds)

def assign_class(ds, func_fill_classroom, schedule, course, section, func_optimal_ts):
    teacher = ds["ClassTeacher"][course]
    if teacher in ds["TeacherBusy"]:
        timeslotsTeacherFree = ds["Timeslots"] - ds["TeacherBusy"][teacher]
    else:
        timeslotsTeacherFree = ds["Timeslots"]
    optimal = func_optimal_ts(timeslotsTeacherFree, ds, course)
    optimalMetric = optimal[0]
    optimalTimeslot = optimal[1]
    if optimalMetric == 0:
        return schedule
    classroom = ds["PossibleClassrooms"][optimalTimeslot].pop(0)[0] # largest classroom available at timeslot
    if not ds["PossibleClassrooms"][optimalTimeslot]:
        ds["PossibleClassrooms"].pop(optimalTimeslot)
    classroomSize = ds["ClassroomSize"][classroom]
    pair = func_fill_classroom(teacher, course, classroomSize, optimalTimeslot, ds, schedule, func_optimal_ts)
    if section:
        course += ".1"
    ds = pair[1]
    studentsInClass = pair[0]
    schedule.append((course, classroom, teacher, optimalTimeslot, studentsInClass))
    return (ds,schedule)

def fill_schedule(ds, schedule, func_fill_classroom, func_optimal_ts):
    while ds["PopularClasses"] and ds["PossibleClassrooms"]:
        class_added = assign_class(ds, func_fill_classroom, schedule, ds["PopularClasses"].pop(0).id, False, func_optimal_ts)
        ds = class_added[0]
        schedule = class_added[1]
    return schedule

def registrars(ds):
    initialize = initialize_schedule(ds, fill_classroom, get_optimal_ts)
    schedule = initialize[0]
    ds = initialize[1]
    schedule = fill_schedule(ds, schedule, fill_classroom, get_optimal_ts)
    return schedule
