from . import db  # Import the database object from the current package
from datetime import datetime  # Import datetime to handle timestamps

# Student model representing the 'students' table in the database
class Student(db.Model):
    __tablename__ = 'students'  # Table name in the database

    # Defining the columns for the 'students' table
    student_id = db.Column(db.Integer, primary_key=True)  # Primary key
    first_name = db.Column(db.String(100), nullable=False)  # First name of the student
    last_name = db.Column(db.String(100), nullable=False)  # Last name of the student
    email = db.Column(db.String(150), unique=True, nullable=False)  # Email (must be unique)
    password = db.Column(db.String(200), nullable=False)  # Hashed password for security
    dob = db.Column(db.Date, nullable=False)  # Date of birth
    phone_number = db.Column(db.String(20), nullable=False)  # Contact number
    address = db.Column(db.String(250), nullable=True)  # Address (optional)
    program = db.Column(db.String(100), nullable=False)  # Program the student is enrolling in
    admission_status = db.Column(db.String(50), default="Submitted")  # Status of admission application
    created_at = db.Column(db.DateTime, default=datetime.now())  # Timestamp of when the record was created

    # Relationships
    admissions = db.relationship('Admission', backref='student', lazy=True)  # One-to-many relationship with Admission
    documents = db.relationship('Document', backref='student', lazy=True)  # One-to-many relationship with Document

    # Method to convert the object into JSON format
    def to_json(self):
        return {
            "studentId": self.student_id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "password": self.password,  # Normally, password wouldn't be exposed like this.
            "dob": self.dob,
            "phoneNumber": self.phone_number,
            "address": self.address,
            "program": self.program,
            "admissionStatus": self.admission_status,
            "createdAt": self.created_at,
        }


# Admission model representing the 'admissions' table in the database
class Admission(db.Model):
    __tablename__ = 'admissions'  # Table name in the database

    # Defining the columns for the 'admissions' table
    admission_id = db.Column(db.Integer, primary_key=True)  # Primary key
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)  # Foreign key linking to student
    status = db.Column(db.String(50), nullable=False, default='Submitted')  # Status of admission (e.g., Submitted, Approved)
    review_notes = db.Column(db.Text, nullable=True)  # Optional notes for review process
    admitted_date = db.Column(db.DateTime)  # Date of admission
    created_at = db.Column(db.DateTime, default=datetime.now())  # Timestamp of when the record was created

    # Method to convert the object into JSON format
    def to_json(self):
        return {
            "admissionId": self.admission_id,
            "studentId": self.student_id,
            "status": self.status,
            "reviewNotes": self.review_notes,
            "admittedDate": self.admitted_date
        }


# Document model representing the 'documents' table in the database
class Document(db.Model):
    __tablename__ = 'documents'  # Table name in the database

    # Defining the columns for the 'documents' table
    document_id = db.Column(db.Integer, primary_key=True)  # Primary key
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)  # Foreign key linking to student
    document_type = db.Column(db.String(100), nullable=False)  # Type of document (e.g., ID, transcript)
    file_path = db.Column(db.String(200), nullable=False)  # File path to where the document is stored
    upload_date = db.Column(db.DateTime, default=datetime.now())  # Date when the document was uploaded
    verification_status = db.Column(db.String(50), default="Pending")  # Status of document verification (Pending, Verified)
    verified_by = db.Column(db.Integer, db.ForeignKey('admins.admin_id'), nullable=True)  # Admin who verified the document
    verification_notes = db.Column(db.Text, nullable=True)  # Optional notes related to verification

    # Method to convert the object into JSON format
    def to_json(self):
        return {
            "documentId": self.document_id,
            "studentId": self.student_id,
            "document_type": self.document_type,
            "filePath": self.file_path,
            "uploadDate": self.upload_date,
            "verificationStatus": self.verification_status,
            "verifiedBy": self.verified_by,
            "verificationNotes": self.verification_notes,
        }


# Admin model representing the 'admins' table in the database
class Admin(db.Model):
    __tablename__ = 'admins'  # Table name in the database

    # Defining the columns for the 'admins' table
    admin_id = db.Column(db.Integer, primary_key=True)  # Primary key
    first_name = db.Column(db.String(100), nullable=False)  # First name of the admin
    last_name = db.Column(db.String(100), nullable=False)  # Last name of the admin
    email = db.Column(db.String(150), unique=True, nullable=False)  # Email (must be unique)
    password = db.Column(db.String(200), nullable=False)  # Hashed password for security
    role = db.Column(db.String(50), default="Admin")  # Role of the admin (default: Admin)
    created_at = db.Column(db.DateTime, default=datetime.now())  # Timestamp of when the record was created

    # Method to convert the object into JSON format
    def to_json(self):
        return {
            "adminId": self.admin_id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "password": self.password,
            "role": self.role
        }
