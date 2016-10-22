def registrars(ds):
    for timeslot in ds["Timeslots"]:
        classroom = ds["PossibleClassrooms"][timeslot].pop() # largest classroom available at timeslot
        course = ds["PopularClasses"].pop() # Most popular class
        ds["Schedule"][timeslot][classroom] = {course: {}}
        while ds["ClassroomSize"][classroom] > 0 or ds["PossibleStudents"][course] != set():
            student = ds["PossibleStudents"][course].pop()
            ds["Schedule"][timeslot][classroom][course].add(student)
            ds["StudentsInTimeslot"][timeslot].add(student)
        teacher = ds["ClassTeacher"][course]
        ds["TeacherBusy"][teacher].add(timeslot)
    return ds["Schedule"]

ds = {
        "Timeslots": [1, 2],
        "PossibleClassrooms": 1: [3, 1, 2],
                              2: [3, 1, 3],,
        

