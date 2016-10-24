from collections import namedtuple
PopularClass = namedtuple('PopularClass', 'id students size')

# returns a dictionary {Class: { set of students that want to take Class }}
def get_possible_students(student_preference_list):
    student_preference_list = student_preference_list
    possible_students = {}
    for student in student_preference_list:
        student_id = student[0]
        student = iter(student)
        next(student) # skip student ID
        for class_preference in student:
            if class_preference in possible_students:
                possible_students[class_preference].add(student_id)
            else:
                possible_students[class_preference] = set([student_id])
    return possible_students

# returns a list of named tuples (class_id, list of students interested, number_of_students_interested)
# Example Usage:
#   most_popular = popular_classes.pop(0)
#   most_popular.id
#   >>> id number
#   most_popular.students
#   >>> list of students
#   most_popular.size
#   >>> number of students interested in class
def get_popular_classes(student_preference_list):
    possible_students = get_possible_students(student_preference_list)
    popular_classes = []
    # Since dictionaries can't be sorted, create a list of
    # named tuples (class id, list of students interested, number of students interested)
    for course, student_list in possible_students.iteritems():
        popular_classes.append(PopularClass(course, student_list, len(student_list)))
    # Now sort in descending order
    popular_classes = sorted(popular_classes, key=lambda x: x[2], reverse=True)
    return popular_classes

# returns a list of tuples (room, room_size) sorted in descending order
def get_rooms(constraints):
    list_of_rooms = []
    for line in constraints:
        if line[0] == 'Rooms':
            number_of_rooms = line[1]
            begin_point = constraints.index(line) + 1 # This is the part of text that marks the beginning of the list of rooms
        elif line[0] == 'Classes':
            end_point = constraints.index(line)

    # This actually creates the list of lists
    for room in constraints[begin_point:end_point]:
        room_number = room[0]
        room_size = int(room[1])
        list_of_rooms.append((room_number, room_size))
    list_of_rooms = sorted(list_of_rooms, key=lambda x: x[1], reverse=True)
    return list_of_rooms

# returns a dictionary ( {room_id: room_size} )
def get_classroom_sizes(constraints):
    return dict(get_rooms(constraints))


# returns a dictionary {Class:Teacher}
def init_class_teacher(constraints):
    for line in constraints:
        if line[0] == 'Teachers':
            breakpoint = constraints.index(line) # This is the part of text that marks the beginning of the list of teahers and classes they teach
            break
    classes_teachers = constraints[breakpoint+1:] # List of list(class, teacher_id)
    return dict(classes_teachers)

#returns a set of timeslots
def get_timeslots(constraints):
    return set([x for x in range(1, int(constraints[0][1])+1)])

# return a dictionary {timeslot: list of classrooms}
def get_possible_classrooms(constraints):
    timeslots = get_timeslots(constraints)
    possible_classrooms = {}
    for timeslot in timeslots:
        possible_classrooms[timeslot] = get_rooms(constraints)
    return possible_classrooms

# Initially, there are no students assigned to any timeslot.
# Returns a dictionary { Timeslot: [list of students assigned to timeslot] }
# def init_students_in_timeslot(constraints):
#     timeslots = get_timeslots(constraints)
#     students_in_timeslot = {}
#     for timeslot in timeslots:
#         students_in_timeslot[timeslot] = [] # empty list of students
#     return students_in_timeslot

def generate(student_preference_list, constraints):
    ds = {}
    ds["Timeslots"] = get_timeslots(constraints)
    ds["PopularClasses"] = get_popular_classes(student_preference_list)
    ds["PossibleClassrooms"] = get_possible_classrooms(constraints)
    ds["PossibleStudents"] = get_possible_students(student_preference_list)
    ds["ClassTeacher"] = init_class_teacher(constraints)
    ds["ClassroomSize"] = get_classroom_sizes(constraints)
    return ds
