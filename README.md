# CST8916 – Remote Data and Real-time Applications

## Assignment 1: REST API Extension

|                  |                              |
| ---------------- | ---------------------------- |
| **Semester**     | Winter 2026                  |
| **Name**         | Mimi Dib                     |
| **Student ID**   | 040829779                    |
| **Date**         | February 6, 2026             |

---

## Demo Video

🎥 [Watch Demo Video](https://youtu.be/sSv9H3zHImg)

## Learning Objectives

Upon successful completion of this assignment, you will be able to:

| 💡  | Objective                                                       |
| --- | --------------------------------------------------------------- |
| ✅  | Demonstrate understanding of RESTful API design principles      |
| ✅  | Extend an existing Flask API with new functionality             |
| ✅  | Implement proper HTTP methods, status codes, and error handling |
| ✅  | Test API endpoints using the REST Client extension              |
| ✅  | Deploy a REST API to Azure App Service                          |

### Reflection
I noticed the local POST, PUT, DELETE works, but in Azure it does not- I found it worked using HTTPS due to security built-in features of Azure App Service

### [✅] Part 1: Add a Tasks Resource

Extend the Flask API to include a new `tasks` resource with the following endpoints:

| Endpoint      | Method | Description                  | Success Code |
| ------------- | ------ | ---------------------------- | ------------ |
| `/tasks`      | GET    | Retrieve all tasks           | 200          |
| `/tasks/<id>` | GET    | Retrieve a single task by ID | 200          |
| `/tasks`      | POST   | Create a new task            | 201          |
| `/tasks/<id>` | PUT    | Update an existing task      | 200          |
| `/tasks/<id>` | DELETE | Delete a task                | 204          |

#### Task Data Structure

Each task must contain the following fields:

```json
{
  "id": 1,
  "title": "Complete Assignment 1",
  "description": "Extend the REST API with tasks",
  "user_id": 1,
  "completed": false
}
```

**Field Specifications:**

| Field         | Type    | Required | Default | Description                        |
| ------------- | ------- | -------- | ------- | ---------------------------------- |
| `id`          | integer | Auto     | —       | Unique identifier (auto-generated) |
| `title`       | string  | Yes      | —       | Task title                         |
| `description` | string  | No       | `""`    | Task description                   |
| `user_id`     | integer | Yes      | —       | Must reference an existing user    |
| `completed`   | boolean | No       | `false` | Task completion status             |

#### Initial Data

Include at least two sample tasks in your in-memory data store:

```python
tasks = [
    {"id": 1, "title": "Learn REST", "description": "Study REST principles", "user_id": 1, "completed": True},
    {"id": 2, "title": "Build API", "description": "Complete the assignment", "user_id": 2, "completed": False},
]
```