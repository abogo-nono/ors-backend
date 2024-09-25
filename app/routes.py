from datetime import datetime
import os

from flask import Blueprint, request, jsonify, make_response, send_file
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

from .models import Student, db, Document, Admission

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def index():
    return make_response(jsonify({'message': 'Online Registration System By ABOGO'}))


"""
    ========= Students Management
"""


@main.route('/get_students', methods=['GET'])
def get_students():
    try:
        students = Student.query.all()

        # Check if there are no students
        if not students:
            return jsonify({"data": []}), 200

        # Convert each student to a dictionary format
        students_data = [student.to_json() for student in students]

        return jsonify({"data": students_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/register_student', methods=['POST'])
def register_student():
    try:
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='scrypt')

        # Convert the dob string to a date object
        dob = datetime.strptime(data['dob'], "%Y-%m-%d").date()

        new_student = Student(
            first_name=data['firstName'],
            last_name=data['lastName'],
            email=data['email'],
            password=hashed_password,
            dob=dob,  # Use the date object here
            phone_number=data['phoneNumber'],
            address=data.get('address'),
            program=data['program']
        )
        db.session.add(new_student)
        db.session.commit()

        return jsonify({"message": "Student registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/get_student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    try:
        student = Student.query.get(student_id)
        if student is None:
            return jsonify({"error": "Student not found"}), 404

        student_data = {
            "firstName": student.first_name,
            "lastName": student.last_name,
            "email": student.email,
            "dob": student.dob.isoformat(),  # Convert date to ISO format
            "phoneNumber": student.phone_number,
            "address": student.address,
            "program": student.program,
            "admissionStatus": student.admission_status,  # Assuming you have this attribute
            "createdAt": student.created_at.isoformat()  # Assuming you have this attribute
        }

        return jsonify({"data": student_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/update_student/<int:student_id>', methods=['PATCH'])
def update_student(student_id):
    try:
        data = request.get_json()
        student = Student.query.get(student_id)

        if student is None:
            return jsonify({"error": "Student not found"}), 404

        # Update fields if provided in the request
        if 'firstName' in data:
            student.first_name = data['firstName']
        if 'lastName' in data:
            student.last_name = data['lastName']
        if 'email' in data:
            student.email = data['email']
        if 'dob' in data:
            # Convert string to date object
            student.dob = datetime.strptime(data['dob'], "%Y-%m-%d").date()
        if 'phoneNumber' in data:
            student.phone_number = data['phoneNumber']
        if 'address' in data:
            student.address = data['address']
        if 'program' in data:
            student.program = data['program']

        db.session.commit()

        return jsonify({"message": "Student updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/delete_student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        student = Student.query.get(student_id)

        # Check if the student exists
        if student is None:
            return jsonify({"error": "Student not found"}), 404

        db.session.delete(student)
        db.session.commit()

        return jsonify({"message": "Student deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


"""
    ========= Documents Management
"""


@main.route('/students/<int:student_id>/documents/<int:document_id>', methods=['GET'])
def get_document(student_id, document_id):
    document = Document.query.filter_by(student_id=student_id, id=document_id).first()

    if not document:
        return jsonify({"error": "Document not found."}), 404

    return jsonify({
        "documentId": document.id,
        "studentId": document.student_id,
        "documentType": document.document_type,
        "filePath": document.file_path,
    }), 200


@main.route('/students/<int:student_id>/documents', methods=['POST'])
def upload_documents(student_id):
    # Check if the request has the file part
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

    # Save file
    filename = secure_filename(file.filename)
    file_path = os.path.join('uploads', filename)

    try:
        file.save(file_path)

        # Create document entry in DB
        new_document = Document(
            student_id=student_id,
            document_type=document_type,
            file_path=file_path
        )
        db.session.add(new_document)
        db.session.commit()

        return jsonify({"message": "Document uploaded successfully!"}), 201

    except Exception as e:
        # Handle exceptions, e.g., file system errors or DB errors
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


def allowed_file(filename):
    # Define allowed file extensions (example)
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/students/<int:student_id>/documents/<int:document_id>/download', methods=['GET'])
def download_document(student_id, document_id):
    document = Document.query.filter_by(student_id=student_id, id=document_id).first()

    if not document:
        return jsonify({"error": "Document not found."}), 404

    # Ensure the file exists before attempting to send it
    if not os.path.isfile(document.file_path):
        return jsonify({"error": "File does not exist."}), 404

    return send_file(document.file_path, as_attachment=True)


@main.route('/students/<int:student_id>/documents/<int:document_id>', methods=['PUT'])
def update_document(student_id, document_id):
    document = Document.query.filter_by(student_id=student_id, id=document_id).first()

    if not document:
        return jsonify({"error": "Document not found."}), 404

    # Check if the request has the file part
    if 'document' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files['document']

    # Validate the file
    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400

    if not file or not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed."}), 400

    document_type = request.form.get('document_type')

    # Save new file
    filename = secure_filename(file.filename)
    file_path = os.path.join('uploads', filename)

    try:
        # Remove the old file if it exists
        if os.path.isfile(document.file_path):
            os.remove(document.file_path)

        # Save the new file
        file.save(file_path)

        # Update the document entry in the DB
        document.document_type = document_type if document_type else document.document_type
        document.file_path = file_path

        db.session.commit()

        return jsonify({"message": "Document updated successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@main.route('/students/<int:student_id>/documents/<int:document_id>', methods=['DELETE'])
def delete_document(student_id, document_id):
    document = Document.query.filter_by(student_id=student_id, id=document_id).first()

    if not document:
        return jsonify({"error": "Document not found."}), 404

    try:
        # Remove the file from the file system
        if os.path.isfile(document.file_path):
            os.remove(document.file_path)

        # Delete the document entry from the database
        db.session.delete(document)
        db.session.commit()

        return jsonify({"message": "Document deleted successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@main.route('/admin/verify_document/<int:document_id>', methods=['POST'])
def verify_document(document_id):
    data = request.get_json()
    document = Document.query.get(document_id)

    if not document:
        return jsonify({"message": "Document not found!"}), 404

    document.verification_status = data['status']
    document.verification_notes = data.get('notes')
    document.verified_by = data['adminId']

    db.session.commit()

    return jsonify({"message": "Document verification updated successfully!"}), 200


"""
    ========= Admission Management
"""


@main.route('/students/<int:student_id>/admission', methods=['GET'])
def check_admission_status(student_id):
    admission = Admission.query.filter_by(student_id=student_id).first()

    if admission:
        return jsonify({
            "status": admission.status,
            "review_notes": admission.review_notes
        }), 200
    else:
        return jsonify({"message": "Admission record not found!"}), 404


@main.route('/students/<int:student_id>/admission', methods=['PATCH'])
def update_admission_status(student_id):
    try:
        data = request.get_json()
        admission = Admission.query.get(student_id)

        if admission is None:
            return jsonify({"message": "Admission record not found!"}), 404

        # Update provided fields
        if 'status' in data:
            admission.status = data['status']
        if 'review_notes' in data:
            admission.review_notes = data['reviewNotes']

        db.session.commit()

        return jsonify({"message": "Admission updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

