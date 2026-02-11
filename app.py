# AI Disclosure: Copilot AI was used with inline suggestions to assist with
# implementing the tasks CRUD endpoints
# improve comments and formatting for better readability and maintainability.
# The code was written by the student, and the AI suggestions were used as a guide to implement the required functionality.

# Import necessary modules from Flask
# Flask: the core framework for the web app
# jsonify: to convert Python dictionaries to JSON responses
# request: to access incoming request data (e.g., POST data)
# abort: to handle errors and send error status codes
from flask import Flask, abort, jsonify, request
from flask_cors import CORS  # Enable Cross-Origin Resource Sharing for client apps

# Initialize the Flask app
app = Flask(__name__)

# Enable CORS so the HTML client can connect from a browser
# This allows requests from different origins (e.g., file:// or another port)
CORS(app)

# In-memory "database" of users
# This list holds a set of user dictionaries.
# In a real-world application, this would be replaced by a database such as MySQL, PostgreSQL, or MongoDB.
users = [
    {"id": 1, "name": "Alice", "age": 25},
    {"id": 2, "name": "Bob", "age": 30},
]

# In-memory "database" of tasks
# This list holds a set of task dictionaries.
tasks = [
    {
        "id": 1,
        "title": "Complete Assignment 1",
        "description": "Extend the REST API with tasks",
        "user_id": 1,
        "completed": False,
    },
    {
        "id": 2,
        "title": "Build API",
        "description": "Complete the assignment",
        "user_id": 2,
        "completed": False,
    },
]


# Define route to handle requests to the root URL ('/')
@app.route("/")
def index():
    return "Welcome to Flask REST API Demo! Try accessing /users to see all users."


# Health check route (GET)
# This endpoint returns a 200 OK status and a JSON response to confirm that the service is running.
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200  # Return HTTP status 200 OK


# User Endpoints


# Route to retrieve all users (GET request)
# When the client sends a GET request to /users, this function will return a JSON list of all users.
# The @ symbol in Python represents a decorator.
# In this case, @app.route is a Flask route decorator.
# It is used to map a specific URL (route) to a function in your Flask application.
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200  # 200 is the HTTP status code for 'OK'


# Route to retrieve a single user by their ID (GET request)
# When the client sends a GET request to /users/<id>, this function will return the user with the specified ID.
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    # Using a list comprehension to find the user by ID
    user = next((user for user in users if user["id"] == user_id), None)
    if user is None:
        abort(404)  # If the user is not found, return a 404 error (Not Found)
    return jsonify(
        user
    ), 200  # Return the user as a JSON object with a 200 status code (OK)


# Route to create a new user (POST request)
# When the client sends a POST request to /users with user data, this function will add the new user to the list.
@app.route("/users", methods=["POST"])
def create_user():
    # If the request body is not in JSON format or if the 'name' field is missing, return a 400 error (Bad Request)
    if not request.json or not "name" in request.json:
        abort(400)

    # Create a new user dictionary. Assign the next available ID by incrementing the highest current ID.
    # If no users exist, the new ID will be 1.
    new_user = {
        "id": users[-1]["id"] + 1 if users else 1,
        "name": request.json["name"],  # The name is provided in the POST request body
        "age": request.json.get(
            "age", 0
        ),  # The age is optional; default is 0 if not provided
    }
    # Add the new user to the users list
    users.append(new_user)
    return jsonify(new_user), 201  # 201 is the HTTP status code for 'Created'


# Route to update an existing user (PUT request)
# When the client sends a PUT request to /users/<id> with updated user data, this function will update the user.
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    # Find the user by their ID
    user = next((user for user in users if user["id"] == user_id), None)
    if user is None:
        abort(404)  # If the user is not found, return a 404 error (Not Found)

    # If the request body is missing or not in JSON format, return a 400 error (Bad Request)
    if not request.json:
        abort(400)

    # Update the user's data based on the request body
    # If a field is not provided in the request, keep the existing value
    user["name"] = request.json.get("name", user["name"])
    user["age"] = request.json.get("age", user["age"])
    return jsonify(
        user
    ), 200  # Return the updated user data with a 200 status code (OK)


# Route to delete a user (DELETE request)
# When the client sends a DELETE request to /users/<id>, this function will remove the user with that ID.
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users  # Reference the global users list
    # Rebuild the users list, excluding the user with the specified ID
    users = [user for user in users if user["id"] != user_id]
    return (
        "",
        204,
    )  # 204 is the HTTP status code for 'No Content', indicating the deletion was successful


# Task Endpoints


# GET all tasks - expected 200 with tasks array
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200  # return all tasks, and 200


# GET a single task - expected 200 with task object
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_tasks_by_id(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        abort(404)  # if task is empty, abort with 404
    return jsonify(task), 200  # return tasks, and 200


# PUT Update a task
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    # Find the task by its ID
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        abort(
            404, description="Task not found"
        )  # If the task is not found, return a 404 error

    # If the request body is missing or not in JSON format, return a 400 error
    if not request.json:
        abort(400, "Request body must be JSON")

    # Update title and description
    task["title"] = request.json.get("title", task["title"])
    task["description"] = request.json.get("description", task["description"])

    # Handle user_id update
    if "user_id" in request.json:  # check if user_id is in the request body
        new_user_id = request.json[
            "user_id"
        ]  # get the new user_id from the request body
        # Check if the new user exists
        if new_user_id not in [user["id"] for user in users]:
            abort(400, f"User with ID {new_user_id} not found")
        task["user_id"] = new_user_id

    # Handle completed update with validation
    if "completed" in request.json:
        completed_value = request.json["completed"]
        if isinstance(completed_value, bool):
            task["completed"] = completed_value
        elif isinstance(completed_value, str):
            if completed_value.lower() not in ["true", "false"]:
                abort(400, "Completed must be true or false")
            task["completed"] = (
                completed_value.lower() == "true"
            )  # convert string to boolean, if value == lowercase true then True else False
        else:
            abort(400, "Completed must be a boolean or string 'true'/'false'")

    return jsonify(task), 200  # Return the updated task data


@app.route("/tasks", methods=["POST"])
def create_task():
    # if request body or 'title' is missing or if user id doesn't exist or if status completed is
    # missing return 400
    # Check if request body exists and is valid JSON
    if not request.json:
        abort(400, "Request body must be JSON")
    # Check required fields
    if "id" not in request.json:
        abort(400, "Task ID is required")
    if "title" not in request.json:
        abort(400, "Title is required")
    if "user_id" not in request.json:
        abort(400, "User ID is required")
    if "completed" not in request.json:
        abort(400, "Completed status is required")

    # Check if task is already exists
    task_id = request.json["id"]
    if any(task["id"] == task_id for task in tasks):
        abort(400, f"Task with ID {task_id} already exists")

    # Check if user_id exists in users (assuming 'users' is a list/dict of valid user IDs)
    if request.json["user_id"] not in [
        user["id"] for user in users
    ]:  # Check the request given value for User item in users array
        abort(400, "User does not exist")

    # Check if completed is a boolean or valid string representation
    completed_value = request.json["completed"]
    if isinstance(completed_value, bool):
        pass  # Valid boolean
    elif isinstance(
        completed_value, str
    ):  # if its a string check if a valid string for a boolean
        if completed_value.lower() not in ["true", "false"]:
            abort(400, "Completed must be true or false")
    else:
        abort(400, "Completed must be a boolean or string 'true'/'false'")

    # if content is valid create task
    new_task = {
        "id": task_id,
        "title": request.json["title"],
        "description": request.json.get(
            "description", "Default Description"
        ),  # The description is optional; default is "Default Description" if not provided
        "user_id": request.json["user_id"],
        "completed": request.json["completed"],
    }

    tasks.append(new_task)  # Add new task to list of tasks
    return jsonify(new_task), 201  # return 201 for Created task


# DELETE a task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks  # Reference the global tasks list
    # Check if task exists
    if task_id not in [task["id"] for task in tasks]:
        abort(404, f"Task with ID {task_id} not found")

    tasks = [task for task in tasks if task["id"] != task_id]
    return (
        "",
        204,
    )  # Return an empty response with 204 status code for successful deletion of task


# Get all tasks for a user
@app.route("/users/<int:user_id>/tasks", methods=["GET"])
def get_user_tasks(user_id):
    # Check if user exists
    if user_id not in [user["id"] for user in users]:
        abort(404, f"User with ID {user_id} not found")
    # filter tasks by user_id
    user_tasks = [task for task in tasks if task["user_id"] == user_id]
    return jsonify(user_tasks), 200  # return user tasks, and 200


# Entry point for running the Flask app
# The app will run on host 0.0.0.0 (accessible on all network interfaces) and port 8000.
# Debug mode is disabled (set to False).
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8000)
