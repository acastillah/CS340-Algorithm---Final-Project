from collections import namedtuple

#extensions: major/minor and class year priority, multiple sections, tri-co bus schedule, classrooms by location, diversity, overlapping timeslots

def fill_classroom(teacher, course, classroomSize, availableStudents, timeslot, ds, schedule):
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
    return (studentsInClass, ds, schedule)

def get_optimal_ts(timeslotsTeacherFree, ds, course):
    metric = float("-inf")
    optimalMetric = float("-inf")
    optimalTimeslot = None
    #figuring out the best timeslot to assign students and class to
    for timeslot in timeslotsTeacherFree:
        classroom = ds["PossibleClassrooms"][timeslot][0][0] #classroom id
        numOfAvailableStudents = len(ds["PossibleStudents"][course] - ds["StudentsInTimeslot"][timeslot])
        classroomSize = 15
        #classroomSize = ds["ClassroomSize"][classroom]
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
        #classroom = None
        course = ds["PopularClasses"].pop(0).id # Most popular class
        # for cm in ds["PossibleClassrooms"][timeslot][0]:
        #     #classroom = ds["PossibleClassrooms"][timeslot][0][0].id # largest classroom available at timeslot
        #     if class_major[course] == building_major[cm.building]:
        #         classroom = cm
        #         break
        # if classroom None:
        #     break
        classroom = ds["PossibleClassrooms"][timeslot].pop(0)[0] # largest classroom available at timeslot
        classroomSize = ds["ClassroomSize"][classroom]
        studentsInClass = []
        ds["StudentsInTimeslot"][timeslot] = set()
        teacher = ds["ClassTeacher"][course]
        pair = func_fill_classroom(teacher, course, classroomSize, ds["PossibleStudents"][course], timeslot, ds, schedule)
        ds = pair[1]
        studentsInClass = pair[0]
        schedule.append((course, classroom, teacher, timeslot, studentsInClass))
        if not ds["PossibleClassrooms"][timeslot]:
            ds["PossibleClassrooms"].pop(timeslot)
    return (schedule, ds)

def assign_class(ds, func_fill_classroom, schedule, course, section):
    teacher = ds["ClassTeacher"][course]
    if teacher in ds["TeacherBusy"]:
        timeslotsTeacherFree = ds["Timeslots"] - ds["TeacherBusy"][teacher]
    else:
        timeslotsTeacherFree = ds["Timeslots"]
    optimal = get_optimal_ts(timeslotsTeacherFree, ds, course)
    optimalMetric = optimal[0]
    optimalTimeslot = optimal[1]
    if optimalMetric == 0:
        return schedule
    classroom = ds["PossibleClassrooms"][optimalTimeslot].pop(0)[0] # largest classroom available at timeslot
    if not ds["PossibleClassrooms"][optimalTimeslot]:
        ds["PossibleClassrooms"].pop(optimalTimeslot)
    classroomSize = ds["ClassroomSize"][classroom]
    availableStudents = ds["PossibleStudents"][course] - ds["StudentsInTimeslot"][optimalTimeslot]
    pair = func_fill_classroom(teacher, course, 10, availableStudents, optimalTimeslot, ds, schedule)
    ds = pair[1]
    studentsInClass = pair[0]
    if section:
        course += ".1"
    schedule.append((course, classroom, teacher, optimalTimeslot, studentsInClass))
    return (ds,schedule)

def fill_schedule(ds, schedule, func_fill_classroom):
    while ds["PopularClasses"] and ds["PossibleClassrooms"]:
        class_added = assign_class(ds, func_fill_classroom, schedule, ds["PopularClasses"].pop(0).id, False)
        ds = class_added[0]
        schedule = class_added[1]
    return schedule

def registrars(ds):
    initialize = initialize_schedule(ds, fill_classroom)
    schedule = initialize[0]
    ds = initialize[1]
    schedule = fill_schedule(ds, schedule, fill_classroom)
    return schedule

# PopularClass = namedtuple('PopularClass', 'id')
#
# ds = {
#     "Timeslots": {1, 2},
#     "PopularClasses": [PopularClass(id="3"),PopularClass(id="2"),PopularClass(id="1"),PopularClass(id="4")],
# }
#
# ds["PossibleClassrooms"] = {1: [("3",8),("1",6),("2",5)], 2: [("3",8),("1",6),("2",5)]}
# ds["PossibleStudents"] = {"1": {"s1","s2","s3","s4"},"2": {"s1","s2","s4","s5","s6"},"3": {"s1","s3","s5","s6","s7"},"4": {"s2","s5","s6","s7"}}
# ds["ClassTeacher"] = {"1": "Jane","2": "Jane","3": "Alex","4": "Connor"}
# ds["ClassroomSize"] = {"1": 6, "2": 5, "3": 8}
#
# print registrars(ds)
