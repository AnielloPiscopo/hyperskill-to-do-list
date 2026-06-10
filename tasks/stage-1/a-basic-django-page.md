# A Basic Django Page

## Description

The **TODO app** helps you keep track of your activity and improve your personal life.
In this project, we will focus on creating an API using the **Django REST Framework** to add tasks and manage our application.

Before creating an actual API, it is important to understand how Django and Django REST Framework communicate with databases and the outcome they produce.

In this stage, you will focus on creating a simple TODO app that will serve as a foundation. You don't need to add fancy templates, user permissions, and authorizations.

Create an app with a `Todo` model that has:
- a **title**
- a **description**
- **two date fields** — one showing when the task was added and one for the deadline
- a **boolean field** to check whether the task has been completed or not

Use the Django **superuser** functionality to add three tasks and a generic **view class** to display them.

Your project should route two URLs:
- `localhost:8000/`
- `localhost:8000/<id>/`

---

## Objectives

In this stage, your program should:

- **Display an unordered list** of all tasks at `localhost:8000/`.  
  For each task, show its:
  - title
  - date of creation
  - deadline date
  - completion status

- **Display a detailed view** of a task by its ID at `localhost:8000/<id>/`.  
  Here, you should also show the task's **description**.

> You don't have to explicitly define the ID parameter in your model, as it is automatically added by Django.

---

## Model Requirements

Your `Todo` model must contain the following fields (use these **exact names**):

| Field            | Type          | Constraints                        |
|------------------|---------------|------------------------------------|
| `task`           | CharField     | max_length = 50                    |
| `description`    | CharField     | max_length = 1024                  |
| `goal_set_date`  | DateTimeField | —                                  |
| `set_to_complete`| DateTimeField | —                                  |
| `is_completed`   | BooleanField  | —                                  |

> ⚠️ Please use these **exact names** for the model and its fields, otherwise your solution might not pass the tests.

- Define `Todo` in the `models.py` module and **migrate** it to the database.

---

## Examples

### Example 1 — Output at `localhost:8000/` (list of all tasks)

```
All Tasks

• Title: Task1
  Goal Set On: Aug. 7, 2021
  Set To Complete: Aug. 8, 2021
  Completed Status: False

• Title: Task2
  Goal Set On: Aug. 6, 2021
  Set To Complete: Aug. 7, 2021
  Completed Status: True

• Title: Task3
  Goal Set On: Aug. 7, 2021
  Set To Complete: Aug. 10, 2021
  Completed Status: False
```

---

### Example 2 — Output at `localhost:8000/1/` (detailed view)

```
Task1
Create a Django TODO-list app.

• Goal Set On: Aug. 7, 2021
• Set To Complete: Aug. 8, 2021
• Completed Status: False
```

> The **description** is visible only in the detailed view, not in the list view.
