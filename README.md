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

This command executes a script that will initialize and create the database locally. It also creates sample data for the tables. 

### Sample Data

#### Users

| username | password |
|----------|----------|
|test1|password1|
|test2|password2|

#### Tasks

| task_id | task | sort_index | user_id |
|----------|----------|----------|----------|
|1|buy milk|0|1|
|2|create proposal for client Co.Bus.|1|1|
|3|water the plants|2|1|

Start the application by running the main application: todolist-app.py

```bash
python todolist-app.py
```
# Authentication

Authentication can be done using a session key. Login using the [login](https://github.com/darljed/todo-list-python-api/edit/dev/README.md#login-authlogin) endpoint `/auth/login`. Successfull login will return a session key. 

The session key will be used to authenticate the succeeding request for task management by setting `Authorization` header to `Key <sessionKey>`

Each session key expires after 10 minutes of inactivity.

Example:

`'Authorization: Key a1d29210e41aade4a0fcbc38ba7842b4e9b7e2be8475ae8d'`


# Endpoints

## Register (/auth/register)

Endpoint for creating new user account.

### POST

#### Request Parameters
- username (String)  
- password (String) 

Example: 

```curl
curl -k -X POST http://localhost:5000/auth/register -d username=johny.dela.cruz -d password=averylongpassword
```

## Login (/auth/login)

Endpoint for authenticating users using username and password.

### POST

#### Request Parameters
- username (String)  
- password (String) 

Example: 

| username | password |
| ----------- | ----------- |
| test1 | password1 |

```curl
curl -k -X POST http://localhost:5000/auth/login -d username=test1 -d password=password1
```

#### Response

Successful login will return a session key. Use the session key to authenticate the succceeding task-related requests. See [Authentication](https://github.com/darljed/todo-list-python-api/edit/dev/README.md#authentication) section for more details.

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

Endpoint for listing all current user's tasks.

### GET

#### Request Parameters

- None

### Requires [Authentication](https://github.com/darljed/todo-list-python-api/edit/dev/README.md#authentication)

Example: 

```curl
curl -k -X GET -H "Authorization: Key {add_session_key_here}" http://localhost:5000/task/list
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

## Create a task (/task/create)

Endpoint for creating a new task for the current authenticated user.

### POST

#### Request Parameters

- task (String)

### Requires [Authentication](https://github.com/darljed/todo-list-python-api/edit/dev/README.md#authentication)

Example: 

```curl
curl -k -X POST -H "Authorization: Key {add_session_key_here}" http://localhost:5000/task/create -d task="Just some task here"
```

#### Response

```bash
{
    "message": {
        "status": "success",
        "content": "A new task has been added"
    },
    "code": 201
}
```
## View task (/task/view/{task_id})

Endpoint for viewing details for a specific task.

### GET

#### Request Parameters

- None

### Requires [Authentication](https://github.com/darljed/todo-list-python-api/edit/dev/README.md#authentication)

Example: 

```curl
curl -k -X GET -H "Authorization: Key {add_session_key_here}" http://localhost:5000/task/view/1
```

#### Response

```curl 
{
    "task": {
        "id": 1,
        "task": "buy milk",
        "sort_index": 0
    },
    "code": 200
}
```

## Update a task (/task/update/{task_id})

Endpoint for updating a specific task of the current authenticated user.

### POST

#### Request Parameters

- task (String)

### Requires [Authentication](https://github.com/darljed/todo-list-python-api/edit/dev/README.md#authentication)

Example: 

```curl
curl -k -X POST -H "Authorization: Key {add_session_key_here}" http://localhost:5000/task/update/4 -d task="Send quotation to client abc"
```

#### Response

```bash
{
    "message": {
        "status": "success",
        "content": "task (id:4) has been successfully updated.",
        "task_id": 4
    },
    "code": 200
}
```

## Delete a task (/task/delete/{task_id})

Endpoint for removing a specific task of the current authenticated user.

### DELETE

#### Request Parameters

- None

### Requires [Authentication](https://github.com/darljed/todo-list-python-api/edit/dev/README.md#authentication)

Example: 

```curl
curl -k -X DELETE -H "Authorization: Key {add_session_key_here}" http://localhost:5000/task/delete/4
```

#### Response

```bash
{
    "message": {
        "status": "success",
        "content": "task (id:4) has been successfully deleted.",
        "task_id": 4
    },
    "code": 200
}
```

## Set sort task position (/task/sort/set/{task_id})

Endpoint for setting a new sorting position to a specific task of the current authenticated user.

### POST

#### Request Parameters

- sort_index (Integer)

### Requires [Authentication](https://github.com/darljed/todo-list-python-api/edit/dev/README.md#authentication)

Example: 

```curl
curl --location -k -X POST -H "Authorization: Key {add_session_key_here}" http://localhost:5000/task/sort/set/1 -d sort_index=2
```

#### Response

```bash
{
    "status": "success",
    "message": {
        "task_fields": [
            "task_id",
            "task",
            "sort_index"
        ],
        "tasks": [
            [
                2,
                "create proposal for client Co.Bus.",
                0
            ],
            [
                3,
                "water the plants",
                1
            ],
            [
                1,
                "buy milk",
                2
            ]
        ]
    },
    "code": 200
}
```

## Bulk set task sort position (/task/sort/set/bulk)

Endpoint for setting a new sorting position to all tasks for current authenticated user.

### POST

#### Request Parameters

- task_ids (Array) - Example: `[2,1,3]`. Task IDs count must match the count of tasks. Task IDs listed must be owned by the current authenticated user.

### Requires [Authentication](https://github.com/darljed/todo-list-python-api/edit/dev/README.md#authentication)

Example: 

```curl
curl --location -k -X POST -H "Authorization: Key {add_session_key_here}" http://localhost:5000/task/sort/set/bulk -d task_ids="[3,2,1]"
```

#### Response

```bash
{
    "message": {
        "status": "success",
        "task_fields": [
            "task_id",
            "task",
            "sort_index"
        ],
        "tasks": [
            [
                3,
                "water the plants",
                0
            ],
            [
                2,
                "create proposal for client Co.Bus.",
                1
            ],
            [
                1,
                "buy milk",
                2
            ]
        ]
    }
}
```
