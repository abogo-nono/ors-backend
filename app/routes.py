from datetime import datetime  # Importing datetime to handle date and time operations
import os  # Importing os to interact with the file system

from flask import Blueprint, request, jsonify, make_response, send_file  # Importing necessary Flask functions
from werkzeug.utils import secure_filename  # Secure filename for file uploads
from werkzeug.security import generate_password_hash  # Secure password hashing

from .models import Student, db, Document, Admission  # Importing database models

# Blueprint to define routes under the "main" namespace
main = Blueprint('main', __name__)

# Route for the index page
@main.route('/', methods=['GET'])
def index():
    # Returns a message as a JSON response
    return make_response(jsonify({'message': 'Online Registration System By ABOGO'}))

"""
    ========= Students Management Routes
"""

# Route to get all students
@main.route('/get_students', methods=['GET'])
def get_students():
    try:
        # Fetch all students from the database
        students = Student.query.all()

        # If there are no students, return an empty list
        if not students:
            return jsonify({"data": []}), 200

        # Convert each student to JSON format
        students_data = [student.to_json() for student in students]

        # Return the student data
        return jsonify({"data": students_data}), 200
    except Exception as e:
        # Return an error message if something goes wrong
        return jsonify({"error": str(e)}), 500

# Route to register a new student
@main.route('/register_student', methods=['POST'])
def register_student():
    try:
        # Get data from the request
        data = request.get_json()
        # Hash the student's password securely
        hashed_password = generate_password_hash(data['password'], method='scrypt')

        # Convert the provided date of birth string to a date object
        dob = datetime.strptime(data['dob'], "%Y-%m-%d").date()

        # Create a new Student instance
        new_student = Student(
            first_name=data['firstName'],
            last_name=data['lastName'],
            email=data['email'],
            password=hashed_password,
            dob=dob,
            phone_number=data['phoneNumber'],
            address=data.get('address'),
            program=data['program']
        )
        # Add the new student to the database
        db.session.add(new_student)
        db.session.commit()

        # Return success message
        return jsonify({"message": "Student registered successfully!"}), 201
    except Exception as e:
        # Return error message if something goes wrong
        return jsonify({"error": str(e)}), 500

# Route to get a specific student by ID
@main.route('/get_student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    try:
        # Find the student by ID
        student = Student.query.get(student_id)
        if student is None:
            return jsonify({"error": "Student not found"}), 404

        # Create a dictionary with the student's information
        student_data = {
            "firstName": student.first_name,
            "lastName": student.last_name,
            "email": student.email,
            "dob": student.dob.isoformat(),  # Convert date to ISO format
            "phoneNumber": student.phone_number,
            "address": student.address,
            "program": student.program,
            "admissionStatus": student.admission_status,  # Assuming admissionStatus exists in the model
            "createdAt": student.created_at.isoformat()  # Convert created date to ISO format
        }

        # Return the student data
        return jsonify({"data": student_data}), 200
    except Exception as e:
        # Return error message if something goes wrong
        return jsonify({"error": str(e)}), 500

# Route to update a student's information
@main.route('/update_student/<int:student_id>', methods=['PATCH'])
def update_student(student_id):
    try:
        # Get the data from the request
        data = request.get_json()
        # Find the student by ID
        student = Student.query.get(student_id)

        if student is None:
            return jsonify({"error": "Student not found"}), 404

        # Update the student's information if provided in the request
        if 'firstName' in data:
            student.first_name = data['firstName']
        if 'lastName' in data:
            student.last_name = data['lastName']
        if 'email' in data:
            student.email = data['email']
        if 'dob' in data:
            # Convert date string to a date object
            student.dob = datetime.strptime(data['dob'], "%Y-%m-%d").date()
        if 'phoneNumber' in data:
            student.phone_number = data['phoneNumber']
        if 'address' in data:
            student.address = data['address']
        if 'program' in data:
            student.program = data['program']

        # Commit the updates to the database
        db.session.commit()

        # Return success message
        return jsonify({"message": "Student updated successfully!"}), 200
    except Exception as e:
        # Return error message if something goes wrong
        return jsonify({"error": str(e)}), 500

# Route to delete a student by ID
@main.route('/delete_student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        # Find the student by ID
        student = Student.query.get(student_id)

        # If the student doesn't exist, return an error
        if student is None:
            return jsonify({"error": "Student not found"}), 404

        # Delete the student from the database
        db.session.delete(student)
        db.session.commit()

        # Return success message
        return jsonify({"message": "Student deleted successfully!"}), 200
    except Exception as e:
        # Return error message if something goes wrong
        return jsonify({"error": str(e)}), 500

"""
    ========= Documents Management Routes
"""

# Route to get a specific document for a student
@main.route('/students/<int:student_id>/documents/<int:document_id>', methods=['GET'])
def get_document(student_id, document_id):
    # Find the document by student ID and document ID
    document = Document.query.filter_by(student_id=student_id, id=document_id).first()

    if not document:
        return jsonify({"error": "Document not found."}), 404

    # Return the document data
    return jsonify({
        "documentId": document.id,
        "studentId": document.student_id,
        "documentType": document.document_type,
        "filePath": document.file_path,
    }), 200

# Route to upload documents for a student
@main.route('/students/<int:student_id>/documents', methods=['POST'])
def upload_documents(student_id):
    # Check if the request contains a file
    if 'document' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files['document']

    # Validate the file and document type
    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400

    if not file or not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed."}), 400

    document_type = request.form.get('document_type')
    if not document_type:
        return jsonify({"error": "Document type is required."}), 400

    # Save the file with a secure filename
    filename = secure_filename(file.filename)
    file_path = os.path.join('uploads', filename)

    try:
        # Save the file to the specified path
        file.save(file_path)

        # Create a new document entry in the database
        new_document = Document(
            student_id=student_id,
            document_type=document_type,
            file_path=file_path
        )
        db.session.add(new_document)
        db.session.commit()

        # Return success message
        return jsonify({"message": "Document uploaded successfully!"}), 201

    except Exception as e:
        # Handle exceptions and roll back the transaction if needed
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Function to check if the file type is allowed (helper function)
def allowed_file(filename):
    # Define allowed file extensions
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to download a specific document for a student
@main.route('/students/<int:student_id>/documents/<int:document_id>/download', methods=['GET'])
def download_document(student_id, document_id):
    # Find the document by student ID and document ID
    document = Document.query.filter_by(student_id=student_id, id=document_id).first()

    if not document:
        return jsonify({"error": "Document not found."}), 404

    # Check if the file exists
    if not os.path.isfile(document.file_path):
        return jsonify({"error": "File does not exist."}), 404

    # Send the file to the user as a downloadable file
    return send_file(document.file_path, as_attachment=True)

# Route to update a specific document for a student
@main.route('/students/<int:student_id>/documents/<int:document_id>', methods=['PUT'])
def update_document(student_id, document_id):
    # Find the document by student ID and document ID
    document = Document.query.filter_by(student_id=student_id, id=document_id).first()

    if not document:
        return jsonify({"error": "Document not found."}), 404

    # Get the new document type from the request
    new_document_type = request.form.get('document_type')
    if not new_document_type:
        return jsonify({"error": "Document type is required."}), 400

    try:
        # Update the document type
        document.document_type = new_document_type
        db.session.commit()

        # Return success message
        return jsonify({"message": "Document updated successfully!"}), 200

    except Exception as e:
        # Handle exceptions and roll back the transaction if needed
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Route to delete a specific document for a student
@main.route('/students/<int:student_id>/documents/<int:document_id>', methods=['DELETE'])
def delete_document(student_id, document_id):
    # Find the document by student ID and document ID
    document = Document.query.filter_by(student_id=student_id, id=document_id).first()

    if not document:
        return jsonify({"error": "Document not found."}), 404

    try:
        # Delete the document entry from the database
        db.session.delete(document)
        db.session.commit()

        # Remove the actual file from the file system
        if os.path.exists(document.file_path):
            os.remove(document.file_path)

        # Return success message
        return jsonify({"message": "Document deleted successfully!"}), 200

    except Exception as e:
        # Handle exceptions and roll back the transaction if needed
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

"""
    ========= Admission Management Routes
"""

# Route to submit admission details for a student
@main.route('/students/<int:student_id>/admissions', methods=['POST'])
def submit_admission(student_id):
    try:
        # Get admission data from the request
        data = request.get_json()

        # Create a new Admission record
        admission = Admission(
            student_id=student_id,
            status=data['status'],
            admitted_at=datetime.now()
        )
        db.session.add(admission)
        db.session.commit()

        # Return success message
        return jsonify({"message": "Admission details submitted successfully!"}), 201

    except Exception as e:
        # Handle exceptions and return error message
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Route to get admission details for a specific student
@main.route('/students/<int:student_id>/admissions', methods=['GET'])
def get_admission(student_id):
    # Find the admission record for the student
    admission = Admission.query.filter_by(student_id=student_id).first()

    if not admission:
        return jsonify({"error": "Admission not found."}), 404

    # Return the admission data
    return jsonify({
        "studentId": admission.student_id,
        "status": admission.status,
        "admittedAt": admission.admitted_at.isoformat(),
    }), 200
