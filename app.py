from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["student_database"]

# Collections
students_collection = db["students"]
lessons_collection = db["lessons"]
subscriptions_collection = db["subscriptions"]

# Function to add a student
def add_student():
    student_number = input("Enter Student Number: ")
    name = input("Enter Name: ")
    nickname = input("Enter Nickname: ")
    age = int(input("Enter Age: "))
    grade = input("Enter Grade: ")
    registration_date = input("Enter Registration Date (YYYY-MM-DD): ")

    # Add student to the students collection
    student_data = {
        "student_number": student_number,
        "name": name,
        "nickname": nickname,
        "age": age,
        "grade": grade,
        "registration_date": registration_date
    }
    students_collection.insert_one(student_data)

    # Add lessons to the lessons collection
    lessons = input("Enter Lessons (pls spread the lessons by comma): ").split(",")
    for lesson in lessons:
        lesson = lesson.strip()
        # Ensure the lesson exists in the lessons collection
        if not lessons_collection.find_one({"lesson_name": lesson}):
            lessons_collection.insert_one({"lesson_name": lesson})

        # Add to subscriptions collection
        lesson_data = lessons_collection.find_one({"lesson_name": lesson})
        subscriptions_collection.insert_one({
            "student_number": student_number,
            "lesson_id": lesson_data["_id"]
        })

    print("Student and lessons added successfully.")

# Function to delete a student
def delete_student():
    student_number = input("Enter Student Number to Delete: ")
    student = students_collection.find_one({"student_number": student_number})
    if student:
        students_collection.delete_one({"student_number": student_number})
        subscriptions_collection.delete_many({"student_number": student_number})
        print("Student deleted successfully.")
    else:
        print("Student not found.")

# Function to update student information
def update_student():
    student_number = input("Enter Student Number to Update: ")
    student = students_collection.find_one({"student_number": student_number})
    if student:
        print("Enter new details (leave blank to keep current values):")
        name = input(f"Name [{student['name']}]: ") or student["name"]
        nickname = input(f"Nickname [{student['nickname']}]: ") or student["nickname"]
        age = input(f"Age [{student['age']}]: ") or student["age"]
        grade = input(f"Grade [{student['grade']}]: ") or student["grade"]
        registration_date = input(f"Registration Date [{student['registration_date']}]: ") or student["registration_date"]

        # Update student information
        students_collection.update_one(
            {"student_number": student_number},
            {"$set": {
                "name": name,
                "nickname": nickname,
                "age": int(age),
                "grade": grade,
                "registration_date": registration_date
            }}
        )
        print("Student information updated successfully.")
    else:
        print("Student not found.")

# Function to show student information
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
        
        # Fetch lessons
        subscriptions = subscriptions_collection.find({"student_number": student_number})
        lesson_names = [lessons_collection.find_one({"_id": sub["lesson_id"]})["lesson_name"] for sub in subscriptions]
        print(f"Lessons: {', '.join(lesson_names)}")
    else:
        print("Student not found.")

# Main menu
def main():
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

# Run the application
if __name__ == "__main__":
    main()
