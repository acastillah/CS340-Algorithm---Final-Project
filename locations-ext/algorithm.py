from generate_data_structures_location import generate

#extensions: major/minor and class year priority, multiple sections, tri-co bus schedule, classrooms by location, diversity, overlapping timeslots

def fill_classroom(teacher, course, classroomSize, timeslot, ds, schedule):
    studentsInClass = []
    availableStudents = ds["PossibleStudents"][course.id] - ds["StudentsInTimeslot"][timeslot]
    while classroomSize > 0 and availableStudents:
        student = availableStudents.pop()
        studentsInClass.append(student)
        ds["StudentsInTimeslot"][timeslot].add(student)
        classroomSize -= 1
    ds["PossibleStudents"][course.id] = availableStudents | ds["StudentsInTimeslot"][timeslot]
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
        classroom = None
        if timeslot not in ds["PossibleClassrooms"]:
            continue
        for possible_classroom in ds["PossibleClassrooms"][timeslot]: # list of classroom objects
            if ds["ClassMajor"][course.id] in ds["BuildingMajor"][possible_classroom.building]:
                classroom = possible_classroom
                break
        if classroom == None:
            classroom = ds["PossibleClassrooms"][timeslot][0]
        numOfAvailableStudents = len(ds["PossibleStudents"][course.id] - ds["StudentsInTimeslot"][timeslot])
        classroomSize = ds["ClassroomSize"][classroom.id]
        if classroomSize > numOfAvailableStudents:
            metric = numOfAvailableStudents
        else:
            metric = classroomSize
        if metric > optimalMetric:
            optimalTimeslot = timeslot
            optimalMetric = metric
    return (optimalMetric, optimalTimeslot)

def initialize_schedule(ds, func_fill_classroom):
    schedule = []
    ds["TeacherBusy"] = {}
    ds["StudentsInTimeslot"] = {}
    for timeslot in ds["Timeslots"]:
        classroom = None
        course = ds["PopularClasses"].pop(0) # Most popular class
        for possible_classroom in ds["PossibleClassrooms"][timeslot]: # list of classroom objects
            if ds["ClassMajor"][course.id] in ds["BuildingMajor"][possible_classroom.building]:
                classroom = possible_classroom
                break
        if classroom == None:
            classroom = ds["PossibleClassrooms"][timeslot].pop(0) # largest classroom available at timeslot
        else:
            ds["PossibleClassrooms"][timeslot].remove(classroom)
        classroomSize = ds["ClassroomSize"][classroom.id]
        studentsInClass = []
        ds["StudentsInTimeslot"][timeslot] = set()
        teacher = ds["ClassTeacher"][course.id]
        pair = func_fill_classroom(teacher, course, classroomSize, timeslot, ds, schedule)
        ds = pair[1]
        studentsInClass = pair[0]
        schedule.append((course.id, classroom.id, teacher, timeslot, studentsInClass))
        if not ds["PossibleClassrooms"][timeslot]:
            ds["PossibleClassrooms"].pop(timeslot)
    return (schedule, ds)

def assign_class(ds, func_fill_classroom, schedule, course, section):
    teacher = ds["ClassTeacher"][course.id]
    if teacher in ds["TeacherBusy"]:
        timeslotsTeacherFree = ds["Timeslots"] - ds["TeacherBusy"][teacher]
    else:
        timeslotsTeacherFree = ds["Timeslots"]
    optimal = get_optimal_ts(timeslotsTeacherFree, ds, course)
    optimalMetric = optimal[0]
    optimalTimeslot = optimal[1]
    if optimalMetric == 0:
        return schedule
    classroom = None
    for possible_classroom in ds["PossibleClassrooms"][optimalTimeslot]: # list of classroom objects
        if ds["ClassMajor"][course.id] in ds["BuildingMajor"][possible_classroom.building]:
            classroom = possible_classroom
            break
    if classroom == None:
        classroom = ds["PossibleClassrooms"][optimalTimeslot].pop(0) # largest classroom available at timeslot
    else:
        ds["PossibleClassrooms"][optimalTimeslot].remove(classroom)
    if not ds["PossibleClassrooms"][optimalTimeslot]:
        ds["PossibleClassrooms"].pop(optimalTimeslot)
    classroomSize = ds["ClassroomSize"][classroom.id]
    pair = func_fill_classroom(teacher, course, classroomSize, optimalTimeslot, ds, schedule)
    if section:
        course.id += ".1"
    ds = pair[1]
    studentsInClass = pair[0]
    schedule.append((course.id, classroom.id, teacher, optimalTimeslot, studentsInClass))
    return (ds,schedule)

def fill_schedule(ds, schedule, func_fill_classroom):
    while ds["PopularClasses"] and ds["PossibleClassrooms"]:
        class_added = assign_class(ds, func_fill_classroom, schedule, ds["PopularClasses"].pop(0), False)
        ds = class_added[0]
        schedule = class_added[1]
    return schedule

def registrars(ds):
    initialize = initialize_schedule(ds, fill_classroom)
    schedule = initialize[0]
    ds = initialize[1]
    schedule = fill_schedule(ds, schedule, fill_classroom)
    return schedule
