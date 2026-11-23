# CodeCraftHub

CodeCraftHub is a beginner-friendly Flask REST API for tracking courses you want to learn. It lets you add, view, update, and delete courses. Course data is saved in a local JSON file, so no database setup is needed.

This project is intended for learning and local use. It does not include authentication or user accounts.

## Features

- Create, view, update, and delete courses.
- Save course data in `courses.json`.
- Automatically create `courses.json` if it does not exist.
- Automatically assign each course an integer ID, starting at `1`.
- Record a creation timestamp for each course.
- Validate required fields, dates, and course statuses.
- Return JSON responses and HTTP status codes.

Each course has these fields:

|
 Field 
|
 Description 
|
|
---
|
---
|
|
`id`
|
 Automatically assigned integer ID 
|
|
`name`
|
 Required course name 
|
|
`description`
|
 Required course description 
|
|
`target_date`
|
 Required date in 
`YYYY-MM-DD`
 format 
|
|
`status`
|
 Required: 
`Not Started`
, 
`In Progress`
, or 
`Completed`
|
|
`created_at`
|
 Automatically generated timestamp 
|

## Project structure

```text
codecrafthub/
├── app.py             # Flask application and API endpoints
├── courses.json       # Course data; created automatically if missing
├── requirements.txt   # Python dependencies (optional)
└── README.md          # Project instructions
```

The JSON file contains an array of course objects. For example:

```json
[
  {
    "id": 1,
    "name": "Flask REST APIs",
    "description": "Learn how to build APIs with Flask.",
    "target_date": "2026-12-15",
    "status": "Not Started",
    "created_at": "2026-11-23T12:00:00+00:00"
  }
]
```

## Installation

### 1. Install Python

Install Python 3 from [python.org](https://www.python.org/downloads/). During installation on Windows, select **Add Python to PATH** if that option is shown.

Check that Python is available:

```bash
python --version
```

Some systems use `python3` instead:

```bash
python3 --version
```

### 2. Open the project folder

In a terminal, move into the folder containing `app.py`:

```bash
cd path/to/codecrafthub
```

### 3. Create and activate a virtual environment

A virtual environment keeps this project's Python packages separate from other projects.

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows Command Prompt:**

```bat
python -m venv .venv
.venv\Scripts\activate
```

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 4. Install Flask

```bash
pip install Flask
```

If the project includes `requirements.txt`, install its dependencies with:

```bash
pip install -r requirements.txt
```

### 5. Check the data file

The application creates `courses.json` automatically when it starts. You can also create it yourself with this initial content:

```json
[]
```

The file should be in the same directory as `app.py`.

## Run the application

Start the Flask server from the project directory:

```bash
python app.py
```

If your system uses `python3`, run:

```bash
python3 app.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

Leave the server running while you send requests from a second terminal. Stop it with `Ctrl+C`.

> The app runs with Flask debug mode enabled in this beginner project. Use it only for local development—not for a public production server.

## API endpoints

The API accepts and returns JSON. For the examples below, `curl` is used to send requests from a terminal.

|
 Method 
|
 Endpoint 
|
 Purpose 
|
 Typical success response 
|
|
---
|
---
|
---
|
---
|
|
`POST`
|
`/api/courses`
|
 Add a course 
|
`201 Created`
|
|
`GET`
|
`/api/courses`
|
 Get all courses 
|
`200 OK`
|
|
`GET`
|
`/api/courses/<id>`
|
 Get one course 
|
`200 OK`
|
|
`PUT`
|
`/api/courses/<id>`
|
 Replace a course's editable fields 
|
`200 OK`
|
|
`DELETE`
|
`/api/courses/<id>`
|
 Delete a course 
|
`204 No Content`
|

Use the course ID in place of `<id>`, for example `/api/courses/1`. The API's collection URL is `/api/courses` (without a trailing slash).

### Create a course

Send all required fields. Do not include `id` or `created_at`; the server generates them.

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Flask REST APIs",
    "description": "Learn how to build APIs with Flask.",
    "target_date": "2026-12-15",
    "status": "Not Started"
  }'
```

A successful response has status `201 Created` and looks like this. The ID and timestamp depend on your data and when you send the request.

```json
{
  "id": 1,
  "name": "Flask REST APIs",
  "description": "Learn how to build APIs with Flask.",
  "target_date": "2026-12-15",
  "status": "Not Started",
  "created_at": "2026-11-23T12:00:00+00:00"
}
```

### Get all courses

```bash
curl -i http://127.0.0.1:5000/api/courses
```

A successful response has status `200 OK` and returns a JSON array. If there are no courses, the response is:

```json
[]
```

### Get one course

```bash
curl -i http://127.0.0.1:5000/api/courses/1
```

A successful response has status `200 OK` and returns the matching course object. If that ID does not exist, the API returns `404 Not Found`.

### Update a course

`PUT` replaces the course's editable fields. Include **all four required fields** in the request, even if you are changing only one. The original `id` and `created_at` are preserved.

```bash
curl -i -X PUT http://127.0.0.1:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Flask REST APIs",
    "description": "Build and test REST APIs with Flask.",
    "target_date": "2027-01-15",
    "status": "In Progress"
  }'
```

A successful response has status `200 OK` and returns the updated course.

### Delete a course

```bash
curl -i -X DELETE http://127.0.0.1:5000/api/courses/1
```

A successful deletion returns `204 No Content` with an empty response body. Deleting an ID that does not exist returns `404 Not Found`.

## Error responses and validation

The API returns a JSON object with an `error` message when it detects a request or storage problem.

|
 Situation 
|
 HTTP status 
|
|
---
|
---:
|
|
 Missing required fields or invalid values 
|
`400 Bad Request`
|
|
 Course ID does not exist 
|
`404 Not Found`
|
|
 JSON file cannot be read or written 
|
`500 Internal Server Error`
|

Required fields are `name`, `description`, `target_date`, and `status`. Dates must be valid calendar dates in `YYYY-MM-DD` format. Allowed statuses are exactly `Not Started`, `In Progress`, and `Completed`.

Example invalid status request:

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Example course",
    "description": "Testing invalid status handling.",
    "target_date": "2026-12-15",
    "status": "Paused"
  }'
```

This returns `400 Bad Request` with an error explaining the allowed status values.

## Testing the API

You can test the endpoints manually with the `curl` examples above. A useful first test sequence is:

1. Start the server.
2. Create a course with `POST`.
3. List courses with `GET /api/courses`.
4. Get the new course by its ID.
5. Update it with `PUT`.
6. Delete it with `DELETE`.
7. Try getting it again and confirm that you receive `404 Not Found`.

To make the first created course use ID `1`, start with an empty `courses.json` containing `[]`. **This removes existing course data**, so only reset the file if you are comfortable doing that.

**macOS / Linux:**

```bash
printf '[]\n' > courses.json
```

**Windows Command Prompt:**

```bat
echo []> courses.json
```

## Troubleshooting

### `curl: (7) Failed to connect`

The Flask server may not be running, or it may be using a different address. Start it with `python app.py` and use `http://127.0.0.1:5000`.

### `python` or `pip` is not recognized

Try `python3` instead of `python`, or `pip3` instead of `pip`. Also check that Python was added to your system's PATH.

### Flask cannot be imported

Activate your virtual environment, then install Flask:

```bash
pip install Flask
```

### The API returns `400 Bad Request`

Check that:

- The request body is valid JSON.
- The request includes all required fields.
- `target_date` is a real date in `YYYY-MM-DD` format.
- `status` exactly matches one of the three allowed values.
- The `Content-Type: application/json` header is included.

### The API returns `404 Not Found`

Check that the course ID exists and that the URL includes the correct ID, such as `/api/courses/1`.

### The API returns `500 Internal Server Error`

Check the terminal where Flask is running for the error details. The app may not have permission to read or write `courses.json`, or the file may contain invalid JSON. If you do not need the existing data, you can reset the file to `[]`.

## Notes for learners

- `GET` reads data, `POST` creates data, `PUT` updates data, and `DELETE` removes data.
- Each endpoint returns an HTTP status code to describe the result.
- This project stores data in a JSON file for simplicity. It is intended for learning and small local projects; it does not provide database features such as safe handling of many simultaneous writes.
- The API has no authentication or user management. Do not expose it publicly with private data.