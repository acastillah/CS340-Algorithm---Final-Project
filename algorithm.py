def registrars(ds):
    for timeslot in ds["Timeslots"]:
        classroom = ds["PossibleClassrooms"][timeslot].pop(0) # largest classroom available at timeslot
        course = ds["PopularClasses"].pop(0) # Most popular class
        ds["Schedule"][timeslot][classroom] = {course: {}}
        #changed the way we use classroom size to go through the loop because the way you had it before you never updated it
        classroomSize = ds["ClassroomSize"][classroom] 
        while classroomSize > 0 or ds["PossibleStudents"][course] != set():
            student = ds["PossibleStudents"][course].pop(0)
            ds["Schedule"][timeslot][classroom][course].add(student)
            ds["StudentsInTimeslot"][timeslot].add(student)
            classroomSize -= 1
        teacher = ds["ClassTeacher"][course]
        ds["TeacherBusy"][teacher].add(timeslot)

    while ds["PopularClasses"] != set() or ds["PossibleClassrooms"] != set():
        course = ds["PopularClasses"].pop(0)
        teacher = ds["ClassTeacher"][course]
        timeslotsTeacherFree = ds["Timeslots"] - ds["TeacherBusy"][teacher]
        metric = float("-inf")
        optimalMetric = float("-inf")
        optimalTimeslot = None
        for timeslot in timeslotsTeacherFree:
            classroom = ds["PossibleClassrooms"][timeslot].pop(0) # largest classroom available at timeslot
            numOfAvailableStudents = abs(ds["PossibleStudents"][course] - ds["Students in Timeslot"][timeslot])
            classroomSize = ds["ClassroomSize"][classroom]
            if classroomSize > numOfAvailableStudents:
                metric = classroomSize
            else:
                metric = numOfAvailableStudents
            if metric > optimalMetric:
                optimalTimeslot = timeslot
                optimalMetric = metric
        if optimalMetric == 0: # why do we have this check??
            break
        classroom = ds["PossibleClassrooms"][optimalTimeslot].pop(0) # largest classroom available at timeslot
        if classroom == None:
            #ds["PossibleClassrooms"][timeslot].remove() #not sure which of these is the right way to do it
            ds["PossibleClassrooms"].remove(timeslot)
        classroomSize = ds["ClassroomSize"][classroom]
        while classroomSize > 0 or ds["PossibleStudents"][course] != set():
            student = ds["PossibleStudents"][course].pop(0)
            ds["Schedule"][optimalTimeslot][classroom][course].add(student)
            ds["StudentsInTimeslot"][optimalTimeslot].add(student)
            classroomSize -= 1
        teacher = ds["ClassTeacher"][course]
        ds["TeacherBusy"][teacher].add(optimalTimeslot)
    return ds["Schedule"]


        

