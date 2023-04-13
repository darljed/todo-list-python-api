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

- Requires python version 3.7 and above (Tested and developed on Python 3.9)
- Modules listed on requirements.txt

### Installation of dependency modules

```bash
pip install -r requirements.txt
```
