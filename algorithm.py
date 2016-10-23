def registrars(ds):
    for timeslot in ds["Timeslots"]:
        classroom = ds["PossibleClassrooms"][timeslot].pop(0) # largest classroom available at timeslot
        course = ds["PopularClasses"].pop(0) # Most popular class
        ds["Schedule"][timeslot][classroom] = {course: set()}
        #changed the way we use classroom size to go through the loop because the way you had it before you never updated it
        classroomSize = ds["ClassroomSize"][classroom]
        #changed the condition because it is not a set but a list (possiblestudents)
        while classroomSize > 0 and ds["PossibleStudents"][course]:
            student = ds["PossibleStudents"][course].pop(0)
            ds["Schedule"][timeslot][classroom][course].add(student)
            ds["StudentsInTimeslot"][timeslot].add(student)
            classroomSize -= 1
        teacher = ds["ClassTeacher"][course]
        ds["TeacherBusy"][teacher].add(timeslot)
        if not ds["PossibleClassrooms"][timeslot]:
            ds["PossibleClassrooms"].pop(timeslot)
    
    while ds["PopularClasses"] and ds["PossibleClassrooms"]:
        course = ds["PopularClasses"].pop(0)
        teacher = ds["ClassTeacher"][course]
        timeslotsTeacherFree = ds["Timeslots"] - ds["TeacherBusy"][teacher]
        metric = float("-inf")
        optimalMetric = float("-inf")
        optimalTimeslot = None
        #figuring out the best timeslot to assign students and class to
        for timeslot in timeslotsTeacherFree:
            classroom = ds["PossibleClassrooms"][timeslot][-1:]
            numOfAvailableStudents = len(ds["PossibleStudents"][course] - ds["StudentsInTimeslot"][timeslot])
            classroomSize = ds["ClassroomSize"][classroom.pop(0)]
            if classroomSize > numOfAvailableStudents:
                metric = numOfAvailableStudents
            else:
                metric = classroomSize
            if metric > optimalMetric:
                optimalTimeslot = timeslot
                optimalMetric = metric
        if optimalMetric == 0: 
            break
        #need to check this cuz i dont think it's right as is
        classroom = ds["PossibleClassrooms"][optimalTimeslot].pop(0) # largest classroom available at timeslot
        if not ds["PossibleClassrooms"][optimalTimeslot]:
            ds["PossibleClassrooms"].pop(optimalTimeslot)
        classroomSize = ds["ClassroomSize"][classroom]
        ds["Schedule"][optimalTimeslot][classroom] = {course: set()}
        availableStudents = ds["PossibleStudents"][course] - ds["StudentsInTimeslot"][optimalTimeslot]
        #while classroomSize > 0 and ds["PossibleStudents"][course]:
        while classroomSize > 0 and availableStudents:
            #student = ds["PossibleStudents"][course].pop(0)
            student = availableStudents.pop(0)
            ds["Schedule"][optimalTimeslot][classroom][course].add(student)
            ds["StudentsInTimeslot"][optimalTimeslot].add(student)
            classroomSize -= 1
        teacher = ds["ClassTeacher"][course]
        ds["TeacherBusy"][teacher].add(optimalTimeslot)

    return ds["Schedule"]

ds = {
    "Timeslots": {1, 2},
    "PopularClasses": ["A","D","B","C"],
}

ds["PossibleClassrooms"] = {1: [2,1,3], 2: [2,1,3]}
ds["PossibleStudents"] = {"A": {"s1","s2","s3","s4"},"B": {"s1","s2","s4","s5","s6"},"C": {"s1","s3","s5","s6","s7"},"D": {"s2","s5","s6","s7"}}
ds["ClassTeacher"] = {"A": "Jane","B": "Jane","C": "Alex","D": "Connor"}
ds["TeacherBusy"] = {"Jane": set(), "Alex": set(), "Connor": set()}
ds["StudentsInTimeslot"] = {1: set(),2:set()}
ds["ClassroomSize"] = {1: 6, 2: 5, 3: 8}
ds["Schedule"] = {1: {}, 2:{}}
ds["Schedule"][1] = {1:{},2:{},3:{}}
ds["Schedule"][2] = {1:{},2:{},3:{}}

registrars(ds)
print ds["Schedule"]
