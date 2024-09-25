# Student Management Endpoints API Documentation

## Overview

The Student Management API allows you to manage student records. You can register new students, retrieve student information, update existing records, and delete students from the database.

## Base URL

```
http://yourapi.com/api
```

## Endpoints

1. ### Register Student

- **Endpoint:** `/register_student`
- **Method:** `POST`
- **Description:** Registers a new student in the system.

**Request Body:**

```json
{
    "firstName": "Abogo",
    "lastName": "Nono",
    "email": "abogo.nono@example.com",
    "password": "securePassword123",
    "dob": "2000-01-01",
    "phoneNumber": "123-456-7890",
    "address": "123 Main St, Anytown, CM",
    "program": "Computer Science"
}
```

**Responses:**

- **201 Created**

```json
{
    "message": "Student registered successfully!"
}
```

- **500 Internal Server Error**

```json
{
    "error": "Error message"
}
```

2. ### Get Student by ID

- **Endpoint:** `/get_student/<int:student_id>`
- **Method:** `GET`
- **Description:** Retrieves detailed information about a specific student by their `ID`.

**Path Parameters:**

- `student_id` (integer): The unique `ID` of the student.

**Responses:**

- **200 OK**

```json
{
    "data": {
    "firstName": "Abogo",
    "lastName": "Nono",
    "email": "abogo.nono@example.com",
        "dob": "2000-01-01",
        "phoneNumber": "123-456-7890",
        "address": "123 Main St, Anytown, CM",
        "program": "Computer Science"
    }
}

```

**404 Not Found**

```json
{
    "error": "Student not found"
}
```

- 500 **Internal Server Error**

```json
{
    "error": "Error message"
}
```

### 3. Get All Students

- **Endpoint: /students**
- **Method: GET**
- **Description: Retrieves a list of all registered students.**

**Responses:**
**200 OK**

```json
{
    "data": [
        {
      "firstName": "Abogo",
      "lastName": "Nono",
      "email": "abogo.nono@example.com",
            "dob": "2000-01-01",
            "phoneNumber": "123-456-7890",
            "address": "123 Main St, Anytown, USA",
            "program": "Computer Science"
        },
        ...
    ]
}
```

- **500 Internal Server Error**

```json
{
    "error": "Error message"
}
```

### 4. Update Student

- **Endpoint:** `/update_student/<int:student_id>`
- **Method**: `PATCH`
- **Description:** Updates an existing student’s information.
**Path Parameters:**
- `student_id`: The `ID` of the student to update.

**Request Body:**

```json
{
    "firstName": "Jane",
    "lastName": "Doe",
    "email": "jane.doe@example.com",
    "dob": "1999-12-31",
    "phoneNumber": "987-654-3210",
    "address": "456 Another St, Othertown, USA",
    "program": "Software Engineering"
}
```

**Responses:**

- **200 OK**

```json
{
    "message": "Student updated successfully!"
}
```

- **404 Not Found**

```json
{
    "error": "Student not found"
}
```

- **400 Bad Request**

```json
{
    "error": "Validation error message"
}
```

- **500 Internal Server Error**

```json
{
    "error": "Error message"
}
```

### 5. Delete Student

- **Endpoint:** `/delete_student/<int:student_id>`
- **Method:** `DELETE`
- **Description:** Deletes a student by their `ID`.

**Path Parameters:**

- `student_id`: The `ID` of the student to delete.
**Responses:**

**200 OK**

```json
{
    "message": "Student deleted successfully!"
}
```

**404 Not Found**

```json
{
    "error": "Student not found"
}
```

**500 Internal Server Error**

```json
{
    "error": "Error message"
}
```

## Notes

- Ensure that all required fields are included in the request body for creating or updating a student.
- The date format for `dob` should be `YYYY-MM-DD`.
- Handle error responses appropriately in your application to enhance
