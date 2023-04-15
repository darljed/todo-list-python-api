SECRET_KEY = "QnXzFa4zaCElshXN96oiNeMRxAQPzJoB"

SETTINGS = {
    'session':{
        'duration_mins': 10
    }
}

AUTH_URLS = {
    'AuthRegister':'/auth/register',
    'AuthLogin':'/auth/login'
}

TASK_URLS = {
    'TaskList':'/task/list',
    'TaskCreate':'/task/create',
    'TaskView':'/task/view/<int:task_id>',
    'TaskUpdate':'/task/update/<int:task_id>',
    'TaskDelete':'/task/delete/<int:task_id>'
}