from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Student Model
class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.String(10), nullable=False)  # Format: YYYY-MM-DD
    amount_due = db.Column(db.Float, nullable=False)

# Create Database Tables
with app.app_context():
    db.create_all()

# Home Route
@app.route("/")
def home():
    return "Flask CRUD API is Running!"

#create student post
@app.route("/students", methods=["POST"])
def add_student():
    data = request.json
    new_student = Student(
        first_name=data["first_name"],
        last_name=data["last_name"],
        dob=data["dob"],
        amount_due=data["amount_due"]
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student added successfully"}), 201

# Read a Student (GET)
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({
        "student_id": student.student_id,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "dob": student.dob,
        "amount_due": student.amount_due
    })

# Update Student (PUT)
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.json
    student.first_name = data.get("first_name", student.first_name)
    student.last_name = data.get("last_name", student.last_name)
    student.dob = data.get("dob", student.dob)
    student.amount_due = data.get("amount_due", student.amount_due)

    db.session.commit()
    return jsonify({"message": "Student updated successfully"})

# Delete Student (DELETE)
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"})

# Show All Records (GET)
@app.route("/students", methods=["GET"])
def get_all_students():
    students = Student.query.all()
    return jsonify([{
        "student_id": s.student_id,
        "first_name": s.first_name,
        "last_name": s.last_name,
        "dob": s.dob,
        "amount_due": s.amount_due
    } for s in students])

if __name__ == "__main__":
    app.run(debug=True)