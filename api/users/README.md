## Users API Endpoints

### `GET /api/users/`
Retrieve a list of all users.

**Response**
- Status: 200 OK
- Body:

```json
[
    {
        "id": 1,
        "username": "john.doe",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "teacher"
    },
    {
        "id": 2,
        ...
    }
]
```

### `POST /api/users/`
Create a new user.

**Request**
- Body:

```json
{
    "username": "jane.smith",
    "email": "jane.smith@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "role": "teacher",
    "password": "password123"
}
```

**Response**
- Status: 201 Created
- Body:

```json
{
    "id": 3,
    "username": "jane.smith",
    "email": "jane.smith@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "role": "teacher"
}
```

### `GET /api/users/{pk}/`
Retrieve details of a specific user.

**Response**
- Status: 200 OK
- Body:

```json
{
    "id": 1,
    "username": "john.doe",
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "teacher"
}
```

### `PUT /api/users/{pk}/`
Update details of a specific user.

**Request**
- Body:

```json
{
    "username": "jane.smith",
    "email": "jane.smith@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "role": "teacher"
}
```

**Response**
- Status: 200 OK
- Body:

```json
{
    "id": 2,
    "username": "jane.smith",
    "email": "jane.smith@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "role": "teacher"
}
```

### `DELETE /api/users/{pk}/`
Delete a specific user.

**Response**
- Status: 204 No Content

## Teachers API

### `GET /api/teachers/`
Retrieve a list of all teachers.

**Response**
- Status: 200 OK
- Body:

```json
[
    {
        "id": 1,
        "info" : {
            "first_name" : "John",
            "last_name" : "Doe",
            "last_login" :"2023-06-01" 
        }
    },
    {
        "id": 2,
        ...
    }
]
```

### `POST /api/teachers/`
Create a new teacher.

**Request**
- Body:

```json
{
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "phone": "9876543210",
    "subject": "Science",
    "years_of_experience": 3,
    "institution": 1
}
```

**Response**
- Status: 201 Created
- Body:

```json
{


    "id": 3,
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "phone": "9876543210",
    "subject": "Science",
    "years_of_experience": 3,
    "institution": {
        "id": 1,
        "name": "ABC School"
    }
}
```

### `GET /api/teachers/{pk}/`
Retrieve details of a specific teacher.

**Response**
- Status: 200 OK
- Body:

```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "1234567890",
    "subject": "Mathematics",
    "years_of_experience": 5,
    "institution": {
        "id": 1,
        "name": "ABC School"
    }
}
```

### `PUT /api/teachers/{pk}/`
Update details of a specific teacher.

**Request**
- Body:

```json
{
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "phone": "9876543210",
    "subject": "Science",
    "years_of_experience": 4,
    "institution": 2
}
```

**Response**
- Status: 200 OK
- Body:

```json
{
    "id": 2,
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "phone": "9876543210",
    "subject": "Science",
    "years_of_experience": 4,
    "institution": {
        "id": 2,
        "name": "XYZ School"
    }
}
```

### `DELETE /api/teachers/{pk}/`
Delete a specific teacher.

**Response**
- Status: 204 No Content

## Employees API

### `GET /api/employees/`
Retrieve a list of all employees.

**Response**
- Status: 200 OK
- Body:

```json
[
    {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "position": "Administrative Assistant",
        "department": "Administration"
    },
    {
        "id": 2,
        ...
    }
]
```

### `POST /api/employees/`
Create a new employee.

**Request**
- Body:

```json
{
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "phone": "9876543210",
    "position": "Human Resources Manager",
    "department": "Human Resources"
}
```

**Response**
- Status: 201 Created
- Body:

```json
{
    "id": 3,
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "phone": "9876543210",
    "position": "Human Resources Manager",
    "department": "Human Resources"
}
```

### `GET /api/employees/{pk}/`
Retrieve details of a specific employee.

**Response**
- Status: 200 OK
- Body:

```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "1234567890",
    "position": "Administrative Assistant",
    "department": "Administration"
}
```

### `PUT /api/employees/{pk}/`
Update details of a specific employee

.

**Request**
- Body:

```json
{
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "phone": "9876543210",
    "position": "HR Manager",
    "department": "Human Resources"
}
```

**Response**
- Status: 200 OK
- Body:

```json
{
    "id": 2,
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "phone": "9876543210",
    "position": "HR Manager",
    "department": "Human Resources"
}
```

### `DELETE /api/employees/{pk}/`
Delete a specific employee.

**Response**
- Status: 204 No Content