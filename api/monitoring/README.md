## Monitoring API Endpoints

### `GET /api/announcement/`
Retrieve a list of all announcements.

**Response**
- Status: 200 OK
- Body:

```json
[
    {
        "id": 1,
        "title": "Announcement 1",
        "content": "This is the content of announcement 1",
        "image": null,
        "creation_date": "2023-05-30T10:00:00Z",
        "created_by": {
            "id": 1,
            "username": "john.doe"
        },
        "start_date": "2023-06-01T10:00:00Z",
        "expiration_date": "2023-06-15T10:00:00Z",
        "url": "https://example.com"
    },
    ...
]
```

### `POST /api/announcement/`
Create a new announcement.

**Request**
- Body:

```json
{
    "title": "New Announcement",
    "content": "This is a new announcement.",
    "image": null,
    "start_date": "2023-06-01T10:00:00Z",
    "expiration_date": "2023-06-15T10:00:00Z",
    "url": "https://example.com",
    "group_id": 1
}
```

**Response**
- Status: 201 Created
- Body: 

```json
{
    "id": 2,
    "title": "New Announcement",
    "content": "This is a new announcement.",
    "image": null,
    "creation_date": "2023-06-01T12:34:56Z",
    "created_by": {
        "id": 1,
        "username": "john.doe"
    },
    "start_date": "2023-06-01T10:00:00Z",
    "expiration_date": "2023-06-15T10:00:00Z",
    "url": "https://example.com"
}
```

### `GET /api/announcement_user/`
Retrieve a list of all announcement-user relationships.

**Response**
- Status: 200 OK
- Body:

```json
[
    {
        "id": 1,
        "announcement": 1,
        "user": {
            "id": 1,
        },
        "status": "CREATED",
        "read_at": null
    },
    ...
]
```

### `POST /api/announcement_user/`
Create a new announcement-user relationship.

**Request**
- Body:

```json
{
    "announcement": 1,
    "user": 1,
    "status": "CREATED",
    "read_at": null
}
```

**Response**
- Status: 201 Created
- Body:

```json
{
    "id": 2,
    "announcement": 1,
    "user": {
        "id": 1,
        "username": "john.doe"
    },
    "status": "CREATED",
    "read_at": null
}
```

### `GET /api/form_template/`
Retrieve a list of all form templates.

**Response**
- Status: 200 OK
- Body:

```json
[
    {
        "id": 1,
        "form_type": "Template 1",
        "start_date": "2023-06-01T10:00:00Z",
        "end_date": "2023-06-15T10:00:00Z"
    },
    ...
]
``

`

### `POST /api/form_template/`
Create a new form template.

**Request**
- Body: questions id must be in the order that will be added to the template

```json
{
    "name": "Form 1",
    "form_type": "New Template",
    "status" : "Borrador",
    "start_date": "2023-06-01T10:00:00Z",
    "end_date": "2023-06-15T10:00:00Z",
    "questions" : [1, 2, 3, 4] 
}
```

**Response**
- Status: 201 Created
- Body:

```json
{
    "message": "form template Form 1 created"
}
```

### `GET /api/teacher_form/`
Retrieve a list of all teacher forms.

**Response**
- Status: 200 OK
- Body:

```json
[
    {
        "id": 1,
        "form_template": 1,
        "teacher_profile": {
            "id": 1,
            "username": "john.doe"
        },
        "completed": false,
        "completed_date": null
    },
    ...
]
```

### `POST /api/teacher_form/`
Create a new teacher form.

**Request**
- Body:

```json
{
    "template": 1,
    "teachers" : [
        1,2
    ]
}
```

**Response**
- Status: 201 Created
- Body:

```json
{
    "id": 2,
    "form_template": 1,
    "teacher_profile": {
        "id": 1,
        "username": "john.doe"
    },
    "completed": false,
    "completed_date": null
}
```

### `GET /api/form_question/`
Retrieve a list of all form questions.

**Response**
- Status: 200 OK
- Body:

```json
[
    {
        "id": 1,
        "title": "Question 1",
        "description": "This is question 1.",
        "program": null,
        "created_by": null,
        "creation_date": null,
        "options": false,
        "file": null
    },
    ...
]
```

### `POST /api/form_question/`
Create a new form question.

**Request**
- Body:

```json
{
    "title": "New Question",
    "description": "This is a new question.",
    "program": null,
    "created_by": null,
    "creation_date": null,
    "options": false,
    "file": null
}
```

**Response**
- Status: 201 Created
- Body:

```json
{
    "id": 2,
    "title": "New Question",
    "description": "This is a new question.",
    "program": null,
    "created_by": null,
    "creation_date": null,
    "options": false,
    "file": null
}
```

### `GET /api/form_question_options/`
Retrieve a list of all form question options.

**Response**
- Status: 200 OK
- Body:

```json
[
    {
        "id": 1,
        "question": 1,
        "content": "Option 1"
    },
    ...
]
```

### `POST /api/form_question_options/`
Create a new form question option.

**Request**
- Body:

```json
{
    "question": 1,
    "content": "Option 1"
}
```

**Response**
- Status: 201 Created
- Body:

```json


{
    "id": 2,
    "question": 1,
    "content": "Option 1"
}
```