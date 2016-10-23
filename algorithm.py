def registrars(ds):
    for timeslot in ds["Timeslots"]:
        classroom = ds["PossibleClassrooms"][timeslot].pop() # largest classroom available at timeslot
        course = ds["PopularClasses"].pop() # Most popular class
        ds["Schedule"][timeslot][classroom] = {course: {}} 
        while ds["ClassroomSize"][classroom] > 0 or ds["PossibleStudents"][course] != set(): #where do we update classroom size????
            student = ds["PossibleStudents"][course].pop()
            ds["Schedule"][timeslot][classroom][course].add(student)
            ds["StudentsInTimeslot"][timeslot].add(student)
        teacher = ds["ClassTeacher"][course]
        ds["TeacherBusy"][teacher].add(timeslot)

    while ds["PopularClasses"] != set() or ds["PossibleClassrooms"] != set():
        course = ds["PopularClasses"].pop()
        teacher = ds["ClassTeacher"][course]
        timeslotsTeacherFree = ds["Timeslots"] - ds["TeacherBusy"][teacher]
        metric = float("-inf")
        optimalMetric = float("-inf")
        optimalTimeslot = None
        for timeslot in timeslotsTeacherFree:
            classroom = ds["PossibleClassrooms"][timeslot].pop() # largest classroom available at timeslot
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
        classroom = ds["PossibleClassrooms"][optimalTimeslot].pop() # largest classroom available at timeslot
        if classroom == None:
            ds["PossibleClassrooms"][timeslot].remove() #not sure if this is the right way to do it
        classroomSize = ds["ClassroomSize"][classroom]
        while classroomSize > 0 or ds["PossibleStudents"][course] != set():
            student = ds["PossibleStudents"][course].pop()
            ds["Schedule"][optimalTimeslot][classroom][course].add(student)
            ds["StudentsInTimeslot"][optimalTimeslot].add(student)
            classroomSize -= 1
        teacher = ds["ClassTeacher"][course]
        ds["TeacherBusy"][teacher].add(optimalTimeslot)
    return ds["Schedule"]


        

