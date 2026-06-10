# The Power of API

## Description

In the previous stage, you created a traditional Django page that displays tasks added by the `superuser`. In this stage, you will implement the **same functionality but as an API**.

Like in the previous stage, your model should include:
- a **title**
- a **description**
- **two date fields**
- a **boolean field**

The functionality of these fields is the same as in the previous stage. Writing a **new model** is encouraged since we will continue to improve the project in the following stages. Also, add some tasks using the `superuser` created in the previous stage.

Start by implementing two simple `GET` endpoints:
- `GET /api/tasks`
- `GET /api/tasks/<id>`

These endpoints work similarly to URL routing. While displaying the data, you need to **order the tasks** by:
1. **completion status** — incomplete tasks first
2. **due date** — sooner ones first
3. **date of creation** — older ones first

In the following stages, we will work on `POST` methods as well. For now, you need to use the classes defined in the `generics` module of `rest_framework`: **`ListAPIView`** and **`RetrieveAPIView`**.

```python
from rest_framework import generics
```

> For more information, refer to the [official DRF documentation](https://www.django-rest-framework.org/api-guide/generic-views/).

---

## Objectives

Implement two endpoints:

| Endpoint | Method | Description |
|---|---|---|
| `/api/tasks` | GET | Returns all tasks as a JSON object |
| `/api/tasks/<id>` | GET | Returns the detailed view of a task by its ID |

---

## Examples

### Example 1 — `GET /api/tasks` with 0 tasks

```json
[]
```

### Example 2 — `GET /api/tasks` with three tasks

```json
[
    {
        "id": 1,
        "task": "Task1",
        "description": "Create a django TODO-list app",
        "goal_set_date": "2021-08-07",
        "set_to_complete": "2021-08-08",
        "is_completed": false
    },
    {
        "id": 3,
        "task": "Task3",
        "description": "dsas",
        "goal_set_date": "2021-08-07",
        "set_to_complete": "2021-08-10",
        "is_completed": false
    },
    {
        "id": 2,
        "task": "Task2",
        "description": "aa",
        "goal_set_date": "2021-08-06",
        "set_to_complete": "2021-08-07",
        "is_completed": true
    }
]
```

> Notice the ordering: incomplete tasks first (`is_completed: false`), then ordered by due date, then by creation date.

### Example 3 — `GET /api/tasks/1`

```json
{
    "id": 1,
    "task": "Task1",
    "description": "Create a django TODO-list app",
    "goal_set_date": "2021-08-07",
    "set_to_complete": "2021-08-08",
    "is_completed": false
}
```
