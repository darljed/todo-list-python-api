# Simple ToDo-List Application API
A simple todo-list application created as a requirement for engineering exam.

# Feature Requirements:

##### Register

- The user should be able to register with a username and password
- Usernames must be unique across all users
##### Login
- The user should be able to log in with the credentials they provided in the register endpoint
- Should return an access token that can be used for the other endpoints
##### TODO List
- The user should only be able to access their own tasks
- The user should be able to list all tasks in the TODO list
- The user should be able to add a task to the TODO list
- The user should be able to update the details of a task in their TODO list
- The user should be able to remove a task from the TODO list
- The user should be able to reorder the tasks in the TODO list
- A task in the TODO list should be able to handle being moved more than 50 times
- A task in the TODO list should be able to handle being moved to more than one task away from its current position

# Software Requirements

- Requires python version 3.7 and above (Tested and developed on Python 3.9 on windows 11)
- Modules listed on requirements.txt

### Installation of dependency modules

```bash
pip install -r requirements.txt
```

# Initializing and Starting the Application

Initialize database and creating database tables

```bash
python db-init.py
```

Start the application by running the main application: todolist-app.py

```bash
python todolist-app.py
```

# Usage Example

## Register (/auth/register)

Endpoint for creating user account.

### POST

#### Arguments
- username (String)  
- password (String) 

Example: 

```curl
curl -k -X POST http://localhost:5000/auth/register -d username=johny.dela.cruz -d password=averylongpassword
```

## Login (/auth/login)

Endpoint for authenticating users using username and password.

### POST

#### Arguments
- username (String)  
- password (String) 

Example: 

```curl
curl -k -X POST http://localhost:5000/auth/login -d username=john.dela.cruz -d password=averylongpassword
```

#### Response

Successful login will return a session key. Use the session key to authenticate succceeding task related requests.

```bash
{
    "message": {
        "status": "success",
        "session_key": "a1d29210e41aade4a0fcbc38ba7842b4e9b7e2be8475ae8d",
        "urls": {
            "TaskList": "/task/list",
            "TaskCreate": "/task/create",
            "TaskView": "/task/view/<int:task_id>",
            "TaskUpdate": "/task/update/<int:task_id>",
            "TaskDelete": "/task/delete/<int:task_id>",
            "TaskSetSortIndex": "/task/sort/set/<int:task_id>/",
            "TaskSetSortBulk": "/task/sort/set/bulk"
        }
    },
    "code": 200
}
```

## Task List (/task/list)

Endpoint for creating user account.

### GET

#### Arguments

- None

#### Authentication

Set `Authorization` header to `Key <sessionKey>`

Example:

`'Authorization: Key a1d29210e41aade4a0fcbc38ba7842b4e9b7e2be8475ae8d'`

Example: 

```curl
curl -k -X GET -H "Authorization: Key a1d29210e41aade4a0fcbc38ba7842b4e9b7e2be8475ae8d" http://localhost:5000/task/list
```

#### Response

Successful requests returns an object of tasks for the authenticated user.

```bash
{
    "tasks": [
        {
            "id": 1,
            "task": "buy milk",
            "sort_index": 0
        },
        {
            "id": 2,
            "task": "create proposal for client Co.Bus.",
            "sort_index": 1
        },
        {
            "id": 3,
            "task": "water the plants",
            "sort_index": 2
        }
    ],
    "code": 200
}
```
