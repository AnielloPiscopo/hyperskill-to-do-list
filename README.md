# TO-do List API

A TODO List REST API built with Django and Django REST Framework, developed as part of a HyperSkill project. The API allows users to manage tasks with full CRUD functionality, authentication, and auto-generated documentation.

---

## Features

- **Task management** — create, read, update, and delete tasks
- **Authentication** — session-based authentication with login/logout
- **Permissions** — only the task author can update or delete their tasks
- **User registration** — new users can register via a dedicated endpoint
- **API documentation** — auto-generated Swagger UI via `drf-yasg`
- **SSR views** — server-side rendered list and detail views for tasks

---

## Tech Stack

- Python 3.14
- Django 6.0
- Django REST Framework
- drf-yasg (Swagger documentation)
- SQLite (development)

---

## Installation

### Prerequisites

- Python 3.12+
- pip

### Steps

```bash
# Clone the repository
git clone https://github.com/AnielloPiscopo/hyperskill-to-do-list.git
cd hyperskill-to-do-list

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

---

## API Endpoints

### Tasks

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| GET | `/api/tasks/` | List all tasks | ✅ |
| POST | `/api/tasks/` | Create a new task | ✅ |
| GET | `/api/tasks/<id>/` | Retrieve a task | ✅ |
| PUT | `/api/tasks/<id>/` | Update a task | ✅ Author only |
| PATCH | `/api/tasks/<id>/` | Partially update a task | ✅ Author only |
| DELETE | `/api/tasks/<id>/` | Delete a task | ✅ Author only |

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api-auth/login/` | Login |
| GET | `/api-auth/logout/` | Logout |
| POST | `/register/` | Register a new user |

### SSR Views

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/todo/` | List all tasks (HTML) |
| GET | `/todo/<id>/` | Task detail (HTML) |

### Documentation

| Endpoint | Description |
|----------|-------------|
| `/` | Swagger UI |

---

## Task Model

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Auto-generated |
| `task` | CharField (max 50) | Task title |
| `description` | CharField (max 1024) | Task description |
| `goal_set_date` | DateTimeField | Date the task was created |
| `set_to_complete` | DateTimeField | Deadline |
| `is_completed` | BooleanField | Completion status |
| `todo_of` | ForeignKey (User) | Task author |

---

## Permissions

- **Unauthenticated users** → `403 Forbidden` on all API endpoints
- **Authenticated users** → can view all tasks and create new ones
- **Task author** → can update and delete their own tasks

---

## Project Structure

```
project/
├── django_to_do_list/     ← main project
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── local.py
│   │   ├── auth.py
│   │   ├── drf.py
│   │   └── allauth.py
│   └── urls.py
├── todo/                  ← main app
│   ├── views/
│   │   ├── ssr.py         ← HTML views
│   │   └── api.py         ← API views
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   └── urls.py
└── manage.py
```

---

## Development Stages

This project was developed in 5 stages as part of a HyperSkill course:

- **Stage 1** — Basic Django SSR page with Todo model and list/detail views
- **Stage 2** — REST API with `GET /api/tasks/` and `GET /api/tasks/<id>/`
- **Stage 3** — Full CRUD + authentication and permissions
- **Stage 4** — User registration
- **Stage 5** — API documentation with Swagger UI via `drf-yasg`
