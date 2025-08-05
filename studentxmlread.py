import xml.etree.ElementTree as ET

tree = ET.parse('students.xml')
root = tree.getroot()

print("Student Details:\n")
for student in root.findall('student'):
    student_id = student.get('id')
    name = student.find('name').text
    stdID = student.find('stdID').text
    Program = student.find('Program').text

    print(f"ID: {student_id}")
    print(f"Name: {name}")
    print(f"StudentID: {stdID}")
    print(f"Program: {Program}")
    print("-" * 20)