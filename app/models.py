from . import db
from datetime import datetime


class Student(db.Model):
    __tablename__ = 'students'

    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(250), nullable=True)
    program = db.Column(db.String(100), nullable=False)
    admission_status = db.Column(db.String(50), default="Submitted")
    created_at = db.Column(db.DateTime, default=datetime.now())

    # Relationships
    admissions = db.relationship('Admission', backref='student', lazy=True)
    documents = db.relationship('Document', backref='student', lazy=True)

    def to_json(self):
        return {
            "studentId": self.student_id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "password": self.password,
            "dob": self.dob,
            "phoneNumber": self.phone_number,
            "address": self.address,
            "program": self.program,
            "admissionStatus": self.admission_status,
            "createdAt": self.created_at,
        }


class Admission(db.Model):
    __tablename__ = 'admissions'

    admission_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Submitted')
    review_notes = db.Column(db.Text, nullable=True)
    admitted_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def to_json(self):
        return {
            "admissionId": self.admission_id,
            "studentId": self.student_id,
            "status": self.status,
            "reviewNotes": self.review_notes,
            "admittedDate": self.admitted_date
        }


class Document(db.Model):
    __tablename__ = 'documents'

    document_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    document_type = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.now())
    verification_status = db.Column(db.String(50), default="Pending")
    verified_by = db.Column(db.Integer, db.ForeignKey('admins.admin_id'), nullable=True)
    verification_notes = db.Column(db.Text, nullable=True)

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


class Payment(db.Model):
    __tablename__ = 'payments'

    payment_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.now())
    payment_status = db.Column(db.String(50), nullable=False)
    receipt_url = db.Column(db.String(200), nullable=True)

    def to_json(self):
        return {
            "paymentId": self.payment_id,
            "studentId": self.student_id,
            "amount": self.amount,
            "paymentDate": self.payment_date,
            "paymentStatus": self.payment_status,
            "receiptUrl": self.receipt_url
        }


class Admin(db.Model):
    __tablename__ = 'admins'

    admin_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default="Admin")
    created_at = db.Column(db.DateTime, default=datetime.now())

    def to_json(self):
        return {
            "adminId": self.admin_id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "password": self.password,
            "role": self.role
        }
