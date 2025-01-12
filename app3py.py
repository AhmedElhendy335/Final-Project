from pymongo import MongoClient
from bson import ObjectId  # Important for working with MongoDB 

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["student_database"]

# Collections
students_collection = db["students"]
lessons_collection = db["lessons"]
subscriptions_collection = db["subscriptions"]

# Predefined lessons
predefined_lessons = [
    {"id": 1, "lesson_name": "Math"},
    {"id": 2, "lesson_name": "English"},
    {"id": 3, "lesson_name": "IT"},
    {"id": 4, "lesson_name": "Arabic"},
    {"id": 5, "lesson_name": "Biology"},
    {"id": 6, "lesson_name": "Physics"}
]


def initialize_lessons():
    for lesson in predefined_lessons:
        if not lessons_collection.find_one({"lesson_name": lesson["lesson_name"]}):
            lessons_collection.insert_one({"lesson_name": lesson["lesson_name"]})

# Helper function
def get_integer_input(prompt):
    while True:
        value = input(prompt)
        if value.isdigit():
            return int(value)
        else:
            print("Invalid input. Please enter a valid number.")

# Function to list all predefined lessons
def list_predefined_lessons():
    print("\nAvailable Lessons:")
    for lesson in predefined_lessons:
        print(f"{lesson['id']}. {lesson['lesson_name']}")
    print()

# Function to add a student
def add_student():
    student_number = input("Enter Student Number (numbers only): ")
    if not student_number.isdigit():
        print("Invalid input. Student Number must contain numbers only.")
        return

    name = input("Enter Name: ")
    nickname = input("Enter Nickname: ")
    age = get_integer_input("Enter Age: ")
    grade = input("Enter Grade: ")
    registration_date = input("Enter Registration Date (YYYY-MM-DD): ")

    # Add student
    student_data = {
        "student_number": student_number,
        "name": name,
        "nickname": nickname,
        "age": age,
        "grade": grade,
        "registration_date": registration_date
    }
    students_collection.insert_one(student_data)

    
    print("Now, select lessons for the student:")
    list_predefined_lessons()

    selected_lesson_ids = input("Enter Lesson IDs (comma-separated): ").split(",")
    for lesson_id in selected_lesson_ids:
        lesson_id = lesson_id.strip()
        if lesson_id.isdigit():
            lesson_id = int(lesson_id)
            # Find the lesson by ID
            lesson = next((l for l in predefined_lessons if l["id"] == lesson_id), None)
            if lesson:
                lesson_in_db = lessons_collection.find_one({"lesson_name": lesson["lesson_name"]})
                subscriptions_collection.insert_one({
                    "student_number": student_number,
                    "lesson_id": lesson_in_db["_id"]
                })
            else:
                print(f"Lesson with ID {lesson_id} not found. Skipping.")
        else:
            print(f"Invalid input '{lesson_id}'. Skipping.")

    print("Student and lessons added successfully.")

# delte a student
def delete_student():
    student_number = input("Enter Student Number to Delete: ")
    student = students_collection.find_one({"student_number": student_number})
    if student:
        students_collection.delete_one({"student_number": student_number})
        subscriptions_collection.delete_many({"student_number": student_number})
        print("Student deleted successfully.")
    else:
        print("Student not found.")

# update student information
def update_student():
    student_number = input("Enter Student Number to Update: ")
    student = students_collection.find_one({"student_number": student_number})
    if student:
        print("Enter new details (leave blank to keep current values):")
        name = input(f"Name [{student['name']}]: ") or student["name"]
        nickname = input(f"Nickname [{student['nickname']}]: ") or student["nickname"]
        age = input(f"Age [{student['age']}]: ")
        if age:
            if not age.isdigit():
                print("Invalid age. Keeping the current value.")
                age = student["age"]
            else:
                age = int(age)
        else:
            age = student["age"]
        grade = input(f"Grade [{student['grade']}]: ") or student["grade"]
        registration_date = input(f"Registration Date [{student['registration_date']}]: ") or student["registration_date"]

        # Updateinformation
        students_collection.update_one(
            {"student_number": student_number},
            {"$set": {
                "name": name,
                "nickname": nickname,
                "age": age,
                "grade": grade,
                "registration_date": registration_date
            }}
        )
        print("Student information updated successfully.")
    else:
        print("Student not found.")

#student information
def show_student():
    student_number = input("Enter Student Number to View: ")
    student = students_collection.find_one({"student_number": student_number})
    if student:
        print(f"Student Information:\n"
              f"Number: {student['student_number']}\n"
              f"Name: {student['name']}\n"
              f"Nickname: {student['nickname']}\n"
              f"Age: {student['age']}\n"
              f"Grade: {student['grade']}\n"
              f"Registration Date: {student['registration_date']}\n")

        #lessons
        subscriptions = subscriptions_collection.find({"student_number": student_number})
        lesson_names = [lessons_collection.find_one({"_id": sub["lesson_id"]})["lesson_name"] for sub in subscriptions]
        print(f"Lessons: {', '.join(lesson_names)}")
    else:
        print("Student not found.")

#menu
def main():
    initialize_lessons()  
    while True:
        print("\nMenu:")
        print("A - Add Student")
        print("D - Delete Student")
        print("U - Update Student Info")
        print("S - Show Student Info")
        print("E - Exit")

        choice = input("Enter your choice: ").strip().upper()
        if choice == "A":
            add_student()
        elif choice == "D":
            delete_student()
        elif choice == "U":
            update_student()
        elif choice == "S":
            show_student()
        elif choice == "E":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the thecode
if __name__ == "__main__":
    main()

