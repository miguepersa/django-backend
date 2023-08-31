## Institutions API Endpoints

### `GET /api/institutions/institutions/`
Retrieve a list of all institutions.

**Response**
- Status: 200 OK
- Body:

```json
[
    {
        "id": 1,
        "teachers": [
            {
                "id": 1,
                "name": "John Doe"
            },
            {
                "id": 2,
                "name": "Jane Smith"
            }
        ],
        "short_name": "ABC School",
        "name": "ABC School",
        "organization": "Organization",
        "date_joined": "2023-06-01T12:00:00Z",
        "address": "123 Main St",
        "city": "City",
        "state": "State",
        "monitor": {
            "id": 1,
            "name": "John Doe"
        },
        "classrooms_per_level": 5,
        "students_per_classroom": 30,
        "ocupancy_rate": "90.00",
        "teacher_service": "INT",
        "logo": "/media/logos/logo.jpg"
    },
    {
        "id": 2,
        ...
    }
]
```

### `GET /api/institutions/institutions/{pk}/`
Retrieve details of a specific institution.

**Response**
- Status: 200 OK
- Body:

```json
{
    "id": 1,
    "teachers": [
        {
            "id": 1,
            "name": "John Doe"
        },
        {
            "id": 2,
            "name": "Jane Smith"
        }
    ],
    "short_name": "ABC School",
    "name": "ABC School",
    "organization": "Organization",
    "date_joined": "2023-06-01T12:00:00Z",
    "address": "123 Main St",
    "city": "City",
    "state": "State",
    "monitor": {
        "id": 1,
        "name": "John Doe"
    },
    "classrooms_per_level": 5,
    "students_per_classroom": 30,
    "ocupancy_rate": "90.00",
    "teacher_service": "INT",
    "logo": "/media/logos/logo.jpg"
}
```

### `POST /api/institutions/institutions/`
Create a new institution.

**Request**
- Body:

```json
{
    "teachers": [1, 2],
    "short_name": "ABC School",
    "name": "ABC School",
    "organization": "Organization",
    "address": "123 Main St",
    "city": "City",
    "state": "State",
    "monitor": 1,
    "classrooms_per_level": 5,
    "students_per_classroom": 30,
    "ocupancy_rate": "90.00",
    "teacher_service": "INT",
    "logo": "logo.jpg"
}
```

**Response**
- Status: 201 Created
- Body:

```json
{
    "id": 1,
    "teachers": [
        {
            "id": 1,
            "name": "John Doe"
        },
        {
            "id": 2,
            "name": "Jane Smith"
        }
    ],
    "short_name": "ABC School",
    "name": "ABC School",
    "organization": "Organization",
    "date_joined": "2023-06-01T12:00:00Z",
    "address": "123 Main St

",
    "city": "City",
    "state": "State",
    "monitor": {
        "id": 1,
        "name": "John Doe"
    },
    "classrooms_per_level": 5,
    "students_per_classroom": 30,
    "ocupancy_rate": "90.00",
    "teacher_service": "INT",
    "logo": "/media/logos/logo.jpg"
}
```

### `PUT /api/institutions/institutions/{pk}/`
Update an existing institution.

**Request**
- Body:

```json
{
    "teachers": [1, 2],
    "short_name": "New ABC School",
    "name": "New ABC School",
    "organization": "New Organization",
    "address": "456 Main St",
    "city": "New City",
    "state": "New State",
    "monitor": 2,
    "classrooms_per_level": 6,
    "students_per_classroom": 35,
    "ocupancy_rate": "95.00",
    "teacher_service": "EXT",
    "logo": "new_logo.jpg"
}
```

**Response**
- Status: 200 OK
- Body:

```json
{
    "id": 1,
    "teachers": [
        {
            "id": 1,
            "name": "John Doe"
        },
        {
            "id": 2,
            "name": "Jane Smith"
        }
    ],
    "short_name": "New ABC School",
    "name": "New ABC School",
    "organization": "New Organization",
    "date_joined": "2023-06-01T12:00:00Z",
    "address": "456 Main St",
    "city": "New City",
    "state": "New State",
    "monitor": {
        "id": 2,
        "name": "Jane Smith"
    },
    "classrooms_per_level": 6,
    "students_per_classroom": 35,
    "ocupancy_rate": "95.00",
    "teacher_service": "EXT",
    "logo": "/media/logos/new_logo.jpg"
}
```

### `DELETE /api/institutions/institutions/{pk}/`
Delete an existing institution.

**Response**
- Status: 204 No Content

### `GET /api/institutions/institution_level/`
Retrieve a list of all institution levels.

**Response**
- Status: 200 OK
- Body:

```json
[
    {
        "id": 1,
        "institution": 1,
        "name": "Level 1",
        "stage": "Bachillerato",
        "reference_level": "Reference Level",
        "student_sections": 5,
        "students_per_section": 30,
        "institution_coordinator": {
            "id": 1,
            "name": "John Doe"
        }
    },
    {
        "id": 2,
        ...
    }
]
```

### `GET /api/institutions/institution_level/{pk}/`
Retrieve details of a specific institution level.

**Response**
- Status: 200 OK
- Body:

```json
{
    "id": 1,
    "institution": 1,
    "name": "Level 1",
    "stage": "Bachillerato",
    "reference_level": "Reference Level",
    "student_sections": 5,
    "students_per_section": 30,
    "institution_coordinator": {
        "id": 1,
        "name": "John Doe"
    }
}
```

### `POST /api/institutions/institution_level/`
Create a new institution level.



**Request**
- Body:

```json
{
    "institution": 1,
    "name": "Level 2",
    "stage": "Primaria Menor",
    "reference_level": "Reference Level",
    "student_sections": 4,
    "students_per_section": 25,
    "institution_coordinator": 2
}
```

**Response**
- Status: 201 Created
- Body:

```json
{
    "id": 2,
    "institution": 1,
    "name": "Level 2",
    "stage": "Primaria Menor",
    "reference_level": "Reference Level",
    "student_sections": 4,
    "students_per_section": 25,
    "institution_coordinator": {
        "id": 2,
        "name": "Jane Smith"
    }
}
```

### `PUT /api/institutions/institution_level/{pk}/`
Update an existing institution level.

**Request**
- Body:

```json
{
    "institution": 1,
    "name": "New Level",
    "stage": "Preescolar",
    "reference_level": "New Reference Level",
    "student_sections": 3,
    "students_per_section": 20,
    "institution_coordinator": 2
}
```

**Response**
- Status: 200 OK
- Body:

```json
{
    "id": 2,
    "institution": 1,
    "name": "New Level",
    "stage": "Preescolar",
    "reference_level": "New Reference Level",
    "student_sections": 3,
    "students_per_section": 20,
    "institution_coordinator": {
        "id": 2,
        "name": "Jane Smith"
    }
}
```

### `DELETE /api/institutions/institution_level/{pk}/`
Delete an existing institution level.

**Response**
- Status: 204 No Content

### `GET /api/institutions/{pk}/teachers`
Retrieve a list of teachers associated with an institution.

**Response**
- Status: 200 OK
- Body:

```json
[
    {
        "id": 1,
        "name": "John Doe"
    },
    {
        "id": 2,
        ...
    }
]
```

### `GET /api/institutions/{pk}/courses`
Retrieve a list of courses offered by an institution.

**Response**
- Status: 200 OK
- Body:

```json
[
    {
        "id": 1,
        "name": "Course 1",
        "lessons": {
            "term 1": [
                {
                    "id": 1,
                    "name": "Lesson 1"
                },
                {
                    "id": 2,
                    ...
                }
            ],
            "term 2": [
                ...
            ],
            "term 3": [
                ...
            ]
        },
        "institution_level": "Level 1",
        "program": "Program 1"
    },
    {
        "id": 2,
        ...
    }
]
```

### `GET /api/institutions/{pk}/levels`
Retrieve a list of levels and their courses offered by an institution.

**Response**
- Status: 200 OK
- Body:

```json
{
    "Level 1": [
        {
            "id": 1,
            "name": "Course 1"
        },
        {
            "id": 2,
            ...
        }
    ],
    "Level 2": [
        ...
    ]
}
```

### `POST /api/institutions/institution_upload`
Upload a CSV file to create multiple institutions.

**Request**
- Body:

 Form data with the following fields:
  - `file`: CSV file containing institution data

**Response**
- Status: 200 OK
- Body:

```json
{
    "success": true,
    "message": "Institutions created successfully."
}
```