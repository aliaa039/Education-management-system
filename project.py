import re

class User:
    def __init__(self, id, username, password, full_name, email):
        self.id = id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email

    def validate_email(self):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, self.email)

class Student(User):
    def __init__(self, id, username, password, full_name, email):
        super().__init__(id, username, password, full_name, email)
        self.courses = {}

    def register_course(self, course):
        if course.code not in self.courses:
            self.courses[course.code] = course
            course.add_student(self)

    def unregister_course(self, course_code):
        if course_code in self.courses:
            course = self.courses[course_code]
            del self.courses[course_code]
            course.remove_student(self)

    def view_courses(self):
        for course in self.courses.values():
            print(f"Course Name: {course.name}, Code: {course.code}, Taught by: {course.doctor.full_name}")
            for assignment in course.assignments:
                grade = assignment.grades.get(self.id, "Not graded")
                print(f"Assignment: {assignment.name}, Grade: {grade}")

    def view_grades_report(self):
        for course in self.courses.values():
            total_grade = sum(assign.grades.get(self.id, 0) for assign in course.assignments)
            print(f"Course: {course.code} - Total Assignments: {len(course.assignments)} - Total Grade: {total_grade}")

class Doctor(User):
    def __init__(self, id, username, password, full_name, email):
        super().__init__(id, username, password, full_name, email)
        self.courses = {}

    def create_course(self, name, code):
        course = Course(name, code, self)
        self.courses[code] = course

    def view_courses(self):
        for course in self.courses.values():
            print(f"Course Name: {course.name}, Code: {course.code}")

    def set_grades(self, course_code):
        if course_code in self.courses:
            course = self.courses[course_code]
            for assignment in course.assignments:
                for student_id, solution in assignment.solutions.items():
                    grade = input(f"Enter grade for student {student_id} for assignment {assignment.name}: ")
                    assignment.set_grade(student_id, int(grade))

class TeachingAssistant(User):
    def __init__(id, username, password, full_name, email):
        super().__init__(id, username, password, full_name, email)

class Course:
    def __init__(self, name, code, doctor):
        self.name = name
        self.code = code
        self.doctor = doctor
        self.students = {}
        self.assignments = []

    def add_student(self, student):
        self.students[student.id] = student

    def remove_student(self, student):
        if student.id in self.students:
            del self.students[student.id]

    def create_assignment(self, assignment_name):
        assignment = Assignment(assignment_name, self.code)
        self.assignments.append(assignment)

    def view_course_summary(self, student_id=None):
        print(f"Course: {self.name} ({self.code}) - Taught by: {self.doctor.full_name}")
        for assignment in self.assignments:
            grade = assignment.grades.get(student_id, "Not graded")
            status = "Submitted" if student_id in assignment.solutions else "Not submitted"
            print(f"Assignment: {assignment.name}, Status: {status}, Grade: {grade}")

class Assignment:
    def __init__(self, name, course_code):
        self.name = name
        self.course_code = course_code
        self.solutions = {}
        self.grades = {}

    def submit_solution(self, student_id, solution_text):
        self.solutions[student_id] = solution_text

    def set_grade(self, student_id, grade):
        self.grades[student_id] = grade

    def view_grades_report(self):
        for student_id, grade in self.grades.items():
            print(f"Student ID: {student_id}, Grade: {grade}")

class LMS:
    def __init__(self):
        self.users = {}
        self.current_user = None
        self.load_dummy_data()

    def load_dummy_data(self):
        # Creating some dummy doctors
        doc1 = Doctor(1, "docjohn", "john123", "Dr. John Smith", "john.smith@example.com")
        doc2 = Doctor(2, "docjane", "doc456", "Dr. Jane Doe", "jane.doe@example.com")
        doc3 = Doctor(3, "aliaa", "aliaa11", "Dr. Aliaa Emad", "aliaa.doe@example.com")
        
        # Creating some dummy students
        stu1 = Student(1, "studavid", "password123", "David Johnson", "david.johnson@example.com")
        stu2 = Student(2, "stulisa", "123456", "Lisa Wong", "lisa.wong@example.com")
        stu3 = Student(3, "Alia", "pass123", "Alia Ahmed", "aaa.wong@example.com")

        # Adding users to the system
        self.users[doc1.username] = doc1
        self.users[doc2.username] = doc2
        self.users[doc3.username] = doc3
        self.users[stu1.username] = stu1
        self.users[stu2.username] = stu2
        self.users[stu3.username] = stu3

        # Creating dummy courses
        doc1.create_course("Math 101", "MATH101")
        doc2.create_course("Physics 101", "PHYS101")
        doc3.create_course("Statistics", "STAT211")

        # Registering students to courses
        stu1.register_course(doc1.courses["MATH101"])
        stu2.register_course(doc2.courses["PHYS101"])
        stu3.register_course(doc3.courses["STAT211"])

        # Creating dummy assignments
        doc1.courses["MATH101"].create_assignment("Algebra Homework")
        doc2.courses["PHYS101"].create_assignment("Physics Lab")
        doc3.courses["STAT211"].create_assignment("Statistics Project")

        # Submitting dummy solutions
        doc1.courses["MATH101"].assignments[0].submit_solution(stu1.id, "Algebra Homework Solution by David")
        doc2.courses["PHYS101"].assignments[0].submit_solution(stu2.id, "Physics Lab Report by Lisa")
        doc3.courses["STAT211"].assignments[0].submit_solution(stu3.id, "Statistics Project by AAA")

    def sign_up(self, user_type, id, username, password, full_name, email):
        if user_type == 'doctor':
            user = Doctor(id, username, password, full_name, email)
        elif user_type == 'student':
            user = Student(id, username, password, full_name, email)
        elif user_type == 'ta':
            user = TeachingAssistant(id, username, password, full_name, email)
        if user.validate_email():
            self.users[username] = user
        else:
            print("Invalid email format")

    def sign_in(self, username, password):
        if username in self.users and self.users[username].password == password:
            self.current_user = self.users[username]
        else:
            print("Invalid user name or password")

    def sign_out(self):
        self.current_user = None

    def run(self):
        print("Welcome to the Learning Management System!")
        running = True
        
        while running:
            if not self.current_user:
                running = self.show_main_menu()
            else:
                self.show_user_menu()

    def show_main_menu(self):
        print("\nPlease Enter An Action: ")
        print("\n1. Sign In")
        print("2. Sign Up")
        print("3. Shutdown System")
        choice = input("Enter choice: ")
        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            self.sign_in(username, password)
            if self.current_user:
                print(f"\nWelcome {self.current_user.full_name}. You are logged in.")
            return True
        elif choice == "2":
            user_type = input("User Type (doctor/student/ta): ")
            id = input("ID: ")
            username = input("Username: ")
            password = input("Password: ")
            full_name = input("Full Name: ")
            email = input("Email: ")
            self.sign_up(user_type, id, username, password, full_name, email)
            print ("You Are Signed up ,now you can sign in ")
            return True
        elif choice == "3":
            return False
        else:
            print("Please Enter Valid Input")
            return True

    def show_user_menu(self):
        if isinstance(self.current_user, Doctor):
            self.show_doctor_menu()
        elif isinstance(self.current_user, Student):
            self.show_student_menu()
        elif isinstance(self.current_user, TeachingAssistant):
            self.show_ta_menu()

    def show_doctor_menu(self):
        print("\nPlease Make a Choice:")
        print("1. List Courses")
        print("2. Create Course")
        print("3. View Course")
        print("4. Log Out")
        choice = input("Enter choice: ")
        if choice == "1":
            self.current_user.view_courses()
        elif choice == "2":
            name = input("Course Name: ")
            code = input("Course Code: ")
            self.current_user.create_course(name, code)
        elif choice == "3":
            course_code = input("Course Code: ")
            if course_code in self.current_user.courses:
                self.show_doctor_course_menu(self.current_user.courses[course_code])
        elif choice == "4":
            self.sign_out()

    def show_student_menu(self):
        print("\nPlease Make a Choice:")
        print("1. Register in Course")
        print("2. List My Courses")
        print("3. View a Course")
        print("4. Grades Report")
        print("5. Log Out")
        choice = input("Enter choice: ")
        if choice == "1":
            self.list_and_register_courses()
        elif choice == "2":
            self.current_user.view_courses()
        elif choice == "3":
            course_code = input("Course Code: ")
            if course_code in self.current_user.courses:
                self.show_student_course_menu(self.current_user.courses[course_code])
        elif choice == "4":
            self.current_user.view_grades_report()
        elif choice == "5":
            self.sign_out()

    def show_student_course_menu(self, course):
        while True:
            course.view_course_summary(self.current_user.id)
            print("\nPlease Make a Choice:")
            print("1. Unregister from Course")
            print("2. Submit Assignment Solution")
            print("3. Back")
            choice = input("Enter choice: ")
            if choice == "1":
                course_code = input("Enter course code to unregister: ")
                self.current_user.unregister_course(course_code)
                print(f"You have been unregistered from {course_code}.")
                break
            elif choice == "2":
                assignment_name = input("Enter assignment name: ")
                for assignment in course.assignments:
                    if assignment.name == assignment_name:
                        solution_text = input("Enter solution text: ")
                        assignment.submit_solution(self.current_user.id, solution_text)
                        print("Solution submitted.")
                        break
            elif choice == "3":
                break

    def show_doctor_course_menu(self, course):
        while True:
            print("\nPlease Make a Choice:")
            print("1. List Assignments")
            print("2. Create Assignment")
            print("3. View Assignment")
            print("4. Back")
            choice = input("Enter choice: ")
            if choice == "1":
                course.view_course_summary()
            elif choice == "2":
                assignment_name = input("Assignment Name: ")
                course.create_assignment(assignment_name)
                print(f"Assignment {assignment_name} created.")
            elif choice == "3":
                assignment_name = input("Enter assignment name: ")
                for assignment in course.assignments:
                    if assignment.name == assignment_name:
                        self.show_doctor_assignment_menu(assignment)
                        break
            elif choice == "4":
                break

    def show_doctor_assignment_menu(self, assignment):
        while True:
            print("\nPlease Make a Choice:")
            print("1. Show Info")
            print("2. Show Grades Report")
            print("3. List Solutions")
            print("4. View Solution")
            print("5. Set Grade")
            print("6. Back")
            choice = input("Enter choice: ")
            if choice == "1":
                print(f"Assignment Name: {assignment.name}, Course Code: {assignment.course_code}")
            elif choice == "2":
                assignment.view_grades_report()
            elif choice == "3":
                for student_id, solution in assignment.solutions.items():
                    print(f"Student ID: {student_id}, Solution: {solution}")
            elif choice == "4":
                student_id = input("Enter student ID to view solution: ")
                if student_id in assignment.solutions:
                    print(f"Solution: {assignment.solutions[student_id]}")
                else:
                    print("Solution not found.")
            elif choice == "5":
                student_id = input("Enter student ID to set grade: ")
                grade = input("Enter grade: ")
                assignment.set_grade(student_id, int(grade))
                print("Grade set.")
            elif choice == "6":
                break

    def list_and_register_courses(self):
        available_courses = {code: course for doctor in self.users.values() if isinstance(doctor, Doctor) for code, course in doctor.courses.items()}
        for course_code, course in available_courses.items():
            if course_code not in self.current_user.courses:
                print(f"{course_code}: {course.name}")
        course_code = input("Enter course code to register: ")
        if course_code in available_courses:
            self.current_user.register_course(available_courses[course_code])
            print(f"Successfully registered in {available_courses[course_code].name}")
        else:
            print("Invalid course code")

    def show_ta_menu(self):
        print("1. List Courses")
        print("2. Log Out")
        choice = input("Enter choice: ")
        if choice == "1":
            # TA specific functionality
            pass
        elif choice == "2":
            self.sign_out()

if __name__ == "__main__":
    lms = LMS()
    lms.run()
