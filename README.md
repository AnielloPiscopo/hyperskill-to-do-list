# TO-do List API

A full-stack TODO List application built with Django REST Framework and Vue 3, developed as part of a HyperSkill project and since extended well beyond its original scope. The API lets users organize tasks into boards, manage their lifecycle (soft delete with cascade archiving), and explore the API through auto-generated documentation. The frontend is a Vue 3 SPA that consumes it.

This repository contains both the backend (`project/be`) and the frontend (`project/fe`).

🔗 **Live API:** [https://hyperskill-to-do-list.onrender.com](https://hyperskill-to-do-list.onrender.com)
🔗 **Webpage:** [https://hyperskill-to-do-list.vercel.app](https://hyperskill-to-do-list.vercel.app)

*(Verify these links point to the current deployment before publishing — this document assumes they're up to date.)*

---

## Features

- **Task management** — create, read, update, and delete tasks
- **Board management** — group tasks into boards, with full CRUD
- **Human-readable board URLs** — boards are addressed by an auto-generated slug (e.g. `/boards/my-project/`) rather than a numeric id; renaming a board regenerates its slug while old slugs keep resolving via a redirect
- **Task priority** — assign priority levels to tasks, with automatic ordering by priority and status
- **Soft delete** — archive and restore both tasks and boards instead of permanently deleting them
- **Cascade archiving** — archiving a board archives all of its tasks; restoring a board can optionally restore its tasks too
- **Permanent delete, with guardrails** — a task or board can only be permanently deleted once archived; a board can only be deleted once it has no tasks left, so nothing disappears without an explicit choice
- **Bulk operations** — archive, restore, or permanently delete multiple tasks/boards at once (all, or a specific list of ids)
- **Authentication** — token-based authentication with login, registration, logout, and password change
- **User profile** — retrieve the current user's profile via `/auth/about/`
- **Permissions** — only the author of a task or board can update, delete, archive, or restore it
- **Rate limiting** — login and registration endpoints are throttled to prevent brute force attacks
- **Filtering, search & ordering** — filter tasks by status/priority/board, search by title/description, order by multiple fields
- **Pagination** — consistent page-based pagination across list endpoints
- **API documentation** — auto-generated Swagger UI via `drf-spectacular`
- **Containerized environment** — PostgreSQL via Docker Compose for development
- **Frontend** — Vue 3 + Pinia + Bootstrap 5 single-page app covering the full workflow: auth, board/task CRUD, archive/restore, a trash view with multi-select and bulk actions, and permanent delete with confirmation

---

## Tech Stack

### Backend
- Python 3.14
- Django 6.0
- Django REST Framework
- drf-spectacular (OpenAPI 3 / Swagger documentation)
- PostgreSQL (development, via Docker)
- SQLite (tests)
- Docker / Docker Compose
- Render (deployment)
- Neon (PostgreSQL serverless, production)

### Frontend
- Vue 3 (Composition API, `<script setup>`)
- Vite
- Pinia
- Vue Router
- TypeScript, with types generated from the OpenAPI schema via `openapi-typescript`
- Bootstrap 5
- Axios
- Vercel (deployment)

---

## Repository Structure

```
hyperskill-to-do-list/
├── project/
│   ├── be/       ← Django REST API
│   └── fe/       ← Vue 3 frontend
├── tasks/        ← HyperSkill course task files
├── .gitignore
└── README.md
```

---

## Installation

### Prerequisites

- Python 3.12+
- Node.js 18+
- Docker & Docker Compose
- pip / npm

### Backend

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

### Frontend

```bash
cd hyperskill-to-do-list/project/fe

# Install dependencies
npm install

# Point the frontend at your local API
# (create .env.development with VITE_API_BASE_URL=http://127.0.0.1:8000)

# Regenerate API types from the running backend's OpenAPI schema
npm run generate:types

# Start the dev server
npm run dev
```

The frontend will be available at `http://localhost:5173/`.

---

## API Endpoints

### Authentication

| Method | Endpoint                  | Description                        | Auth required |
|--------|-----------------------------|--------------------------------------|----------------|
| POST   | `/auth/register/`         | Register a new user                | ❌             |
| POST   | `/auth/login/`            | Log in and obtain a token          | ❌             |
| POST   | `/auth/logout/`           | Invalidate the current token       | ✅             |
| GET    | `/auth/about/`            | Retrieve the current user profile  | ✅             |
| POST   | `/auth/change-password/`  | Change the current user's password | ✅             |

### Boards

Boards are addressed by **slug**, not by numeric id (e.g. `/boards/my-project/`). The slug is generated from the title on creation and regenerated whenever the title changes; a `GET` on a previous slug returns a `301` response with the current slug instead of a `404`, so old links and bookmarks keep working after a rename.

| Method | Endpoint                       | Description                                        | Auth required     |
|--------|-----------------------------------|--------------------------------------------------------|--------------------|
| GET    | `/boards/`                     | List all boards                                       | ✅                 |
| POST   | `/boards/`                     | Create a new board                                    | ✅                 |
| GET    | `/boards/<slug>/`               | Retrieve a board, including its active tasks           | ✅ Author only     |
| PUT    | `/boards/<slug>/`               | Fully update a board                                   | ✅ Author only     |
| PATCH  | `/boards/<slug>/`               | Partially update a board                               | ✅ Author only     |
| DELETE | `/boards/<slug>/`               | Permanently delete a board (must be archived and empty) | ✅ Author only     |
| POST   | `/boards/archive-all/`          | Archive all boards, or a subset by ids                 | ✅                 |
| POST   | `/boards/restore-all/`          | Restore all boards, or a subset by ids                 | ✅                 |
| POST   | `/boards/delete-all/`           | Permanently delete all archived boards, or a subset by ids | ✅             |
| POST   | `/boards/<slug>/archive/`       | Archive a board and cascade-archive its tasks           | ✅ Author only     |
| POST   | `/boards/<slug>/restore/`       | Restore a board (optionally its tasks too)              | ✅ Author only     |

`restore-all` and `restore` accept an optional `?restore_tasks=true` query parameter to also restore the tasks associated with the restored board(s).

A board can only be permanently deleted once it is archived **and** has no tasks left attached to it — delete or move its tasks first (or use `delete-all` on the board's tasks). This is a deliberate guardrail: nothing about a board is ever destroyed as a side effect of deleting something else.

### Tasks

| Method | Endpoint                    | Description                                | Auth required     |
|--------|--------------------------------|------------------------------------------------|--------------------|
| GET    | `/tasks/`                     | List all tasks (filter/search/order)           | ✅                 |
| POST   | `/tasks/`                     | Create a new task                              | ✅                 |
| GET    | `/tasks/<id>/`                | Retrieve a task                                | ✅ Author only     |
| PUT    | `/tasks/<id>/`                | Fully update a task                            | ✅ Author only     |
| PATCH  | `/tasks/<id>/`                | Partially update a task                        | ✅ Author only     |
| DELETE | `/tasks/<id>/`                | Permanently delete a task (must be archived)    | ✅ Author only     |
| POST   | `/tasks/archive-all/`         | Archive all tasks, or a subset by ids          | ✅                 |
| POST   | `/tasks/restore-all/`         | Restore all tasks, or a subset by ids          | ✅                 |
| POST   | `/tasks/delete-all/`          | Permanently delete all archived tasks, or a subset by ids | ✅         |
| POST   | `/tasks/<id>/archive/`        | Archive a task                                 | ✅ Author only     |
| POST   | `/tasks/<id>/restore/`        | Restore a task                                 | ✅ Author only     |
| POST   | `/tasks/move/`                | Move a list of tasks to a board (or remove from board) | ✅         |

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

| Field             | Type                              | Description                            |
|--------------------|------------------------------------|-------------------------------------------|
| `id`               | AutoField                        | Auto-generated                          |
| `title`            | CharField (max 50)                | Task title                              |
| `description`      | TextField (max 1024, optional)    | Task description                        |
| `goal_set_date`    | DateField                        | Date the task was created                |
| `set_to_complete`  | DateField                        | Deadline                                |
| `status`           | CharField (enum)                  | `IN_PROGRESS`, `TODO`, `DONE`           |
| `priority`         | CharField (enum)                  | `HIGH`, `MEDIUM`, `LOW`, `ZERO`         |
| `user`             | ForeignKey (User)                  | Task author                             |
| `board`            | ForeignKey (Board, nullable)        | Board the task belongs to. `on_delete=CASCADE`: deleting a board deletes its tasks too (blocked in practice by the board-delete guardrail above) |
| `is_archived`      | BooleanField                      | Soft-delete flag (inherited from `BaseModel`) |
| `created_at` / `updated_at` | DateTimeField              | Timestamps (inherited from `BaseModel`)  |

### Board

| Field             | Type                  | Description                  |
|--------------------|------------------------|---------------------------------|
| `id`               | AutoField              | Auto-generated                |
| `title`            | CharField (max 100)     | Board title                   |
| `slug`             | SlugField (max 100)     | URL identifier, derived from `title`; regenerated on rename (inherited from `SluggedModel`) |
| `description`      | TextField (max 2048)    | Board description              |
| `color`            | CharField (#HEX)        | Display color (e.g. `#FF0000`) |
| `user`             | ForeignKey (User)        | Board author                  |
| `is_archived`      | BooleanField            | Soft-delete flag (inherited from `BaseModel`) |
| `created_at` / `updated_at` | DateTimeField | Timestamps (inherited from `BaseModel`) |

### BaseModel (`core`)

An abstract base model shared by both `Task` and `Board`, providing `is_archived`, `created_at`, `updated_at`, and the `archive()` / `restore()` methods used for soft delete.

### SluggedModel (`core`)

An abstract base model for anything that needs a URL-friendly, renamable identifier — currently `Board`. Generates a unique slug from `title` on save, and records previous slugs in a generic `SlugHistory` table (via Django's content types framework) so that a request for an old slug returns a `301` with the current one instead of a `404`.

---

## Permissions

- **Unauthenticated users** → `401 Unauthorized` on all API endpoints except registration and login
- **Authenticated users** → can view their own tasks/boards and create new ones
- **Author only** → can update, delete, archive, or restore their own tasks/boards (`IsAuthorOrReadOnly`)
- List querysets are scoped to `user=request.user` and, by default, `is_archived=False` (pass `?is_archived=true` to see archived items instead)
- Board detail (`GET`/`PUT`/`PATCH`/`DELETE` on `/boards/<slug>/`) is scoped to `user=request.user` but **not** filtered by `is_archived` — an archived board can still be retrieved directly, which is what lets the frontend show its details from the trash view

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

## Soft Delete, Cascade & Permanent Delete

Rather than permanently deleting tasks and boards outright, the API supports archiving first:

- **Archiving a task** marks it as `is_archived=True`. It disappears from `GET /tasks/` but isn't deleted.
- **Archiving a board** archives the board *and* cascades the archive to all of its active tasks.
- **Restoring a board** restores the board itself. Tasks stay archived unless `?restore_tasks=true` is passed, in which case all of the board's archived tasks are restored too.
- **Permanently deleting a task or board** is only allowed once it's archived. A board additionally requires that it have no tasks left attached to it, so a board can never disappear and silently take unreviewed tasks with it through the API's normal flow.
- **Bulk endpoints** (`archive-all` / `restore-all` / `delete-all`) accept an optional `ids` list in the request body. If `ids` is omitted or empty, the operation applies to all of the user's eligible tasks/boards.

The archive/restore/delete logic lives in dedicated service modules (`task/services`, `board/services`) rather than in the views, keeping the views focused on request/response handling and permission checks.

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
├── core/                      ← shared base models, permissions, validators, slug utilities
│   ├── models/
│   │   ├── base.py
│   │   └── slugs.py
│   ├── utils/
│   │   └── slugs.py
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
│   │   ├── crud.py            ← list, detail, delete-all
│   │   └── soft_delete.py     ← archive, restore, archive-all, restore-all
│   └── tests/
├── task/
│   ├── enums/
│   │   └── choices.py        ← TaskStatus, TaskPriority
│   ├── models/
│   ├── serializers/
│   ├── services/
│   ├── constants/
│   ├── views/
│   │   ├── crud.py            ← list, detail, delete-all
│   │   └── soft_delete.py     ← archive, restore, archive-all, restore-all
│   └── tests/
└── manage.py
```

## Frontend Structure

```
project/fe/
├── src/
│   ├── schema/                ← auto-generated OpenAPI types (openapi-typescript)
│   ├── types/                 ← domain types built on top of the generated schema
│   ├── constants/
│   │   └── endpoints.ts
│   ├── services/              ← one file per domain, thin axios wrappers
│   ├── stores/                ← Pinia stores (auth, board, task)
│   ├── router/
│   ├── composables/
│   ├── components/
│   │   ├── base/               ← generic, reusable, no domain knowledge (e.g. ConfirmModal)
│   │   └── domain/
│   │       ├── auth/
│   │       ├── board/
│   │       └── task/
│   ├── views/
│   ├── App.vue
│   ├── main.ts
│   └── custom.css             ← theme tokens and additive utility classes layered on top of Bootstrap
└── package.json
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

This project was originally developed in 5 stages as part of a HyperSkill course, and has since evolved well beyond that scope with additional features built independently:

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
- Added bulk move endpoint to assign or reassign a list of tasks to a board in a single operation
- Introduced slug-based URLs for boards (`core.SluggedModel`), with automatic redirect from previous slugs after a rename
- Changed `Task.board` to `on_delete=CASCADE`, paired with a guardrail that blocks deleting a board while it still has tasks attached
- Added permanent delete endpoints (single and bulk) for already-archived tasks and boards
- Built the Vue 3 frontend: authentication flow, board and task CRUD with modals, a Trash view with per-item and bulk archive/restore/delete (including multi-select and "select all"), and a Bootstrap-based UI theme
