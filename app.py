from flask import Flask, jsonify, request, make_response
import hashlib

app = Flask(__name__)

# In-memory "database"
students = [
    {"id": 1, "name": "Dorji", "course": "Data Science"},
    {"id": 2, "name": "Choney", "course": "Networking"}
]

# Home route
@app.route("/")
def home():
    return jsonify({"message": "Welcome to Student API"}), 200

# GET all students with Cache-Control & ETag
@app.route("/students", methods=["GET"])
def get_students():
    # Create a simple ETag based on students list
    students_str = str(students).encode()
    etag = hashlib.sha1(students_str).hexdigest()

    # Check if client sent If-None-Match header
    if request.headers.get("If-None-Match") == etag:
        return "", 304  # Not Modified

    # Build response
    response = make_response(jsonify(students), 200)
    response.headers["Cache-Control"] = "public, max-age=60"  # cache for 60 seconds
    response.headers["ETag"] = etag
    return response


# GET single student by ID with Cache-Control & ETag

@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    # Create ETag based on this student's data
    student_str = str(student).encode()
    etag = hashlib.sha1(student_str).hexdigest()

    # Check for If-None-Match header
    if request.headers.get("If-None-Match") == etag:
        return "", 304  # Not Modified

    response = make_response(jsonify(student), 200)
    response.headers["Cache-Control"] = "public, max-age=60"
    response.headers["ETag"] = etag
    return response

# POST, PUT, DELETE remain the same

@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()
    new_student = {
        "id": len(students) + 1,
        "name": data.get("name"),
        "course": data.get("course")
    }
    students.append(new_student)
    return jsonify(new_student), 201

@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    data = request.get_json()
    student["name"] = data.get("name", student["name"])
    student["course"] = data.get("course", student["course"])
    return jsonify(student), 200

@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    global students
    students = [s for s in students if s["id"] != student_id]
    return jsonify({"message": "Student deleted"}), 200

# -------------------------
# HEAD & OPTIONS
# -------------------------
@app.route("/students", methods=["HEAD"])
def head_students():
    return "", 200

@app.route("/students", methods=["OPTIONS"])
def options_students():
    response = app.response_class()
    response.headers["Allow"] = "GET, POST, PUT, DELETE, OPTIONS, HEAD"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, HEAD"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response, 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)
