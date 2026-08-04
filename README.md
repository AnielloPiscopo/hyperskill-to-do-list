# TO-do List API

A TODO List REST API built with Django and Django REST Framework, developed as part of a HyperSkill project. The API allows users to organize tasks into boards, manage their lifecycle (including soft delete with cascade archiving), and explore the API through auto-generated documentation.

This repository contains the backend (`project/be`). A frontend (`project/fe`) may be added in the future.

🔗 **Live API:** [https://hyperskill-to-do-list.onrender.com](https://hyperskill-to-do-list.onrender.com)

---

## Features

- **Task management** — create, read, update, and delete tasks
- **Board management** — group tasks into boards, with full CRUD
- **Task priority** — assign priority levels to tasks, with automatic ordering by priority and status
- **Soft delete** — archive and restore both tasks and boards instead of permanently deleting them
- **Cascade archiving** — archiving a board archives all of its tasks; restoring a board can optionally restore its tasks too
- **Bulk operations** — archive or restore multiple tasks/boards at once (all or a specific list of ids)
- **Authentication** — token-based authentication with login, registration, logout, and password change
- **User profile** — retrieve the current user's profile via `/auth/me/`
- **Permissions** — only the author of a task or board can update, delete, archive, or restore it
- **Rate limiting** — login and registration endpoints are throttled to prevent brute force attacks
- **Filtering, search & ordering** — filter tasks by status/priority/board, search by title/description, order by multiple fields
- **Pagination** — consistent page-based pagination across list endpoints
- **API documentation** — auto-generated Swagger UI via `drf-spectacular`
- **Containerized environment** — PostgreSQL via Docker Compose for development

---

## Tech Stack

- Python 3.14
- Django 6.0
- Django REST Framework
- drf-spectacular (OpenAPI 3 / Swagger documentation)
- PostgreSQL (development, via Docker)
- SQLite (tests)
- Docker / Docker Compose
- Render (deployment)
- Neon (PostgreSQL serverless, production)
- PostgreSQL via Docker Compose (development)

---

## Repository Structure

```
hyperskill-to-do-list/
├── project/
│   ├── be/       ← Django REST API (this document)
│   └── fe/       ← Frontend (planned)
├── tasks/        ← HyperSkill course task files
├── .gitignore
└── README.md
```

---

## Installation

### Prerequisites

- Python 3.12+
- Docker & Docker Compose
- pip

### Steps

```bash
# Clone the repository
git clone https://github.com/AnielloPiscopo/hyperskill-to-do-list.git
cd hyperskill-to-do-list/project/be

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the PostgreSQL container
docker compose up -d

# Apply migrations
docker compose exec web python manage.py migrate

# Create a superuser
docker compose exec web python manage.py createsuperuser
```

The API will be available at `http://localhost:8000/`, with Swagger UI served at the root path.

---

## API Endpoints

### Authentication

| Method | Endpoint                  | Description                        | Auth required |
|--------|----------------------------|------------------------------------|----------------|
| POST   | `/auth/register/`         | Register a new user                | ❌             |
| POST   | `/auth/login/`            | Log in and obtain a token          | ❌             |
| POST   | `/auth/logout/`           | Invalidate the current token       | ✅             |
| GET    | `/auth/me/`               | Retrieve the current user profile  | ✅             |
| POST   | `/auth/change-password/`  | Change the current user's password | ✅             |

### Boards

| Method | Endpoint                     | Description                                  | Auth required     |
|--------|-------------------------------|-----------------------------------------------|--------------------|
| GET    | `/boards/`                   | List all boards                               | ✅                 |
| POST   | `/boards/`                   | Create a new board                            | ✅                 |
| GET    | `/boards/<id>/`               | Retrieve a board, including its active tasks  | ✅ Author only     |
| PUT    | `/boards/<id>/`               | Fully update a board                          | ✅ Author only     |
| PATCH  | `/boards/<id>/`               | Partially update a board                      | ✅ Author only     |
| DELETE | `/boards/<id>/`               | Permanently delete a board                    | ✅ Author only     |
| POST   | `/boards/archive-all/`        | Archive all boards, or a subset by ids        | ✅                 |
| POST   | `/boards/restore-all/`        | Restore all boards, or a subset by ids        | ✅                 |
| POST   | `/boards/<id>/archive/`       | Archive a board and cascade-archive its tasks | ✅ Author only     |
| POST   | `/boards/<id>/restore/`       | Restore a board (optionally its tasks too)    | ✅ Author only     |

`restore-all` and `restore` accept an optional `?restore_tasks=true` query parameter to also restore the tasks associated with the restored board(s).

### Tasks

| Method | Endpoint                    | Description                              | Auth required     |
|--------|-------------------------------|--------------------------------------------|--------------------|
| GET    | `/tasks/`                    | List all tasks (filter/search/order)        | ✅                 |
| POST   | `/tasks/`                    | Create a new task                          | ✅                 |
| GET    | `/tasks/<id>/`                | Retrieve a task                            | ✅ Author only     |
| PUT    | `/tasks/<id>/`                | Fully update a task                        | ✅ Author only     |
| PATCH  | `/tasks/<id>/`                | Partially update a task                    | ✅ Author only     |
| DELETE | `/tasks/<id>/`                | Permanently delete a task                  | ✅ Author only     |
| POST   | `/tasks/archive-all/`         | Archive all tasks, or a subset by ids      | ✅                 |
| POST   | `/tasks/restore-all/`         | Restore all tasks, or a subset by ids      | ✅                 |
| POST   | `/tasks/<id>/archive/`        | Archive a task                             | ✅ Author only     |
| POST   | `/tasks/<id>/restore/`        | Restore a task                             | ✅ Author only     |

**Filtering / search / ordering** on `GET /tasks/`:
- `?status=`, `?priority=` and `?board=` — filter by task status, priority or board
- `?search=` — search by title or description
- `?ordering=` — order by `set_to_complete`, `status`, `priority` or `created_at`

### Documentation

| Endpoint        | Description         |
|-------------------|---------------------|
| `/`                | Swagger UI          |
| `/api/schema/`     | Raw OpenAPI schema  |

---

## Models

### Task

| Field             | Type                          | Description                            |
|--------------------|-------------------------------|------------------------------------------|
| `id`               | AutoField                    | Auto-generated                          |
| `title`            | CharField (max 50)            | Task title                              |
| `description`      | TextField (max 1024)          | Task description                        |
| `goal_set_date`    | DateField                    | Date the task was created                |
| `set_to_complete`  | DateField                    | Deadline                                |
| `status`           | IntegerField (enum)           | `IN_PROGRESS=0`, `TODO=1`, `DONE=2`     |
| `priority`         | IntegerField (enum)           | `HIGH=0`, `MEDIUM=1`, `LOW=2`, `ZERO=3` |
| `user`             | ForeignKey (User)              | Task author                             |
| `board`            | ForeignKey (Board, nullable)    | Board the task belongs to                |
| `is_archived`      | BooleanField                  | Soft-delete flag (inherited from `BaseModel`) |
| `created_at` / `updated_at` | DateTimeField        | Timestamps (inherited from `BaseModel`)  |

### Board

| Field             | Type                  | Description                  |
|--------------------|------------------------|---------------------------------|
| `id`               | AutoField              | Auto-generated                |
| `title`            | CharField (max 100)     | Board title                   |
| `description`      | TextField (max 2048)    | Board description              |
| `color`            | CharField (#HEX)        | Display color (e.g. `#FF0000`) |
| `user`             | ForeignKey (User)        | Board author                  |
| `is_archived`      | BooleanField            | Soft-delete flag (inherited from `BaseModel`) |
| `created_at` / `updated_at` | DateTimeField | Timestamps (inherited from `BaseModel`) |

### BaseModel (`core`)

An abstract base model shared by both `Task` and `Board`, providing `is_archived`, `created_at`, `updated_at`, and the `archive()` / `restore()` methods used for soft delete.

---

## Permissions

- **Unauthenticated users** → `401 Unauthorized` on all API endpoints except registration and login
- **Authenticated users** → can view their own tasks/boards and create new ones
- **Author only** → can update, delete, archive, or restore their own tasks/boards (`IsAuthorOrReadOnly`)
- All list/detail querysets are scoped to `user=request.user` and `is_archived=False`, so archived items are automatically excluded from regular results

---

## Task Ordering

Tasks are automatically ordered by priority and status using the following logic:

```
HIGH priority   + IN_PROGRESS
HIGH priority   + TODO
MEDIUM priority + IN_PROGRESS
MEDIUM priority + TODO
LOW priority    + IN_PROGRESS
LOW priority    + TODO
No priority     + IN_PROGRESS
No priority     + TODO
DONE (regardless of priority)
```

Priority can be assigned to tasks with status `IN_PROGRESS` or `TODO`. Tasks with status `DONE` cannot have a priority other than `ZERO`.

---

## Soft Delete & Cascade Logic

Rather than permanently deleting tasks and boards, the API supports archiving:

- **Archiving a task** marks it as `is_archived=True`. It disappears from `GET /tasks/` but isn't deleted.
- **Archiving a board** archives the board *and* cascades the archive to all of its active tasks.
- **Restoring a board** restores the board itself. Tasks stay archived unless `?restore_tasks=true` is passed, in which case all of the board's archived tasks are restored too.
- **Bulk endpoints** (`archive-all` / `restore-all`) accept an optional `ids` list in the request body. If `ids` is omitted or empty, the operation applies to all of the user's tasks/boards.

The archive/restore logic lives in dedicated service modules (`task/services`, `board/services`) rather than in the views, keeping the views focused on request/response handling and permission checks.

---

## Backend Structure

```
project/be/
├── django_to_do_list/
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── local.py
│   │   ├── auth.py
│   │   └── drf.py
│   └── urls.py
├── core/                      ← shared base model, permissions, validators
│   ├── models/
│   │   └── base.py
│   ├── constants/
│   │   └── api/
│   └── tests/
├── users/                     ← registration, login, logout, profile, password
│   ├── serializers/
│   └── views/
│       ├── login.py
│       ├── logout.py
│       ├── me.py
│       ├── register.py
│       └── change_password.py
├── board/
│   ├── models/
│   ├── serializers/
│   ├── services/
│   ├── constants/
│   ├── views/
│   │   ├── crud.py
│   │   └── soft_delete.py
│   └── tests/
├── task/
│   ├── enums/
│   │   └── choices.py        ← TaskStatus, TaskPriority
│   ├── models/
│   ├── serializers/
│   ├── services/
│   ├── constants/
│   ├── views/
│   │   ├── crud.py
│   │   └── soft_delete.py
│   └── tests/
└── manage.py
```

---

## Running Tests

```bash
# All tests
python manage.py test

# A specific app
python manage.py test task
python manage.py test board

# With Docker
docker compose exec web python manage.py test

# With coverage
docker compose exec web coverage run --source='.' manage.py test
docker compose exec web coverage report
docker compose exec web coverage html
```

---

## Development Stages

This project was originally developed in 5 stages as part of a HyperSkill course, and has since evolved beyond that scope with additional features built independently:

- **Stage 1** — Basic Django SSR page with a Todo model and list/detail views
- **Stage 2** — REST API with `GET /api/tasks/` and `GET /api/tasks/<id>/`
- **Stage 3** — Full CRUD + authentication and permissions
- **Stage 4** — User registration
- **Stage 5** — API documentation with Swagger UI via `drf-yasg`

### Post-HyperSkill improvements

- Renamed the `Todo` model/app to `Task`, replacing the boolean `is_completed` field with a `status` enum (`IN_PROGRESS`, `TODO`, `DONE`)
- Removed server-side rendered (SSR) views in favor of a pure API
- Introduced the `Board` model to group tasks, with its own CRUD endpoints
- Added a shared `BaseModel` in `core` (`is_archived`, `created_at`, `updated_at`) and the `IsAuthorOrReadOnly` permission
- Migrated the development database from SQLite to PostgreSQL, running via Docker Compose
- Implemented soft delete (archive/restore) for tasks and boards, including cascade archiving from boards to their tasks
- Added bulk archive/restore endpoints supporting both "all" and id-based operations
- Migrated API documentation from `drf-yasg` to `drf-spectacular` (OpenAPI 3)
- Added full user profile management: login, logout, profile endpoint, and password change
- Added rate limiting on login and registration endpoints to prevent brute force attacks
- Added `priority` field to tasks (`HIGH`, `MEDIUM`, `LOW`, `ZERO`) with automatic ordering by priority and status
- Added field-level validation: hex color format for boards, date range consistency, board ownership check
