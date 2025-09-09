import json
import os

FILENAME = "student_details.json"

def read_data():
    if not os.path.exists(FILENAME):
        return {"students": []}
    with open(FILENAME, "r") as file:
        return json.load(file)

def write_data(data):
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)

def display_students():
    data = read_data()
    if not data["students"]:
        print("No student records found.")
    else:
        print("\n--- Student Records ---")
        for s in data["students"]:
            print(f"Name: {s['name']}, Age: {s['age']}, Address: {s['address']}")
        print("-----------------------")

def add_student():
    name = input("Enter student name: ")
    age = input("Enter student age: ")
    address = input("Enter student address: ")

    data = read_data()
    new_student = {"name": name, "age": age, "address": address}
    data["students"].append(new_student)
    write_data(data)
    print(f"✅ Added new student: {name}")

def delete_student():
    name = input("Enter student name to delete: ")
    data = read_data()
    updated_students = [s for s in data["students"] if s["name"].lower() != name.lower()]
    
    if len(updated_students) == len(data["students"]):
        print(f"No student found with name: {name}")
    else:
        data["students"] = updated_students
        write_data(data)
        print(f" Deleted student with name: {name}")

def update_student():
    name = input("Enter student name to update: ")
    data = read_data()
    for s in data["students"]:
        if s["name"].lower() == name.lower():
            print("Leave blank if you don’t want to change.")
            new_name= input(f"Enter new name (current: {s['name']}): ")
            new_age = input(f"Enter new age (current: {s['age']}): ")
            new_address = input(f"Enter new address (current: {s['address']}): ")
            if new_name.strip():
                s["name"] = new_name
            if new_age.strip():
                s["age"] = new_age
            if new_address.strip():
                s["address"] = new_address
            write_data(data)
            print(f"Updated student: {name}")
            return
    print(f"No student found with name: {name}")

def menu():
    while True:
        print("\n===== Student Management =====")
        print("1. Display all students")
        print("2. Add a student")
        print("3. Delete a student")
        print("4. Update a student record")
        print("5. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            display_students()
        elif choice == "2":
            add_student()
        elif choice == "3":
            delete_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()
