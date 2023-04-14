from flask_restful import Resource, reqparse
from model import User, Task, Auth
from flask import request

class Helper:
    def msg(self,message,statuscode=None,options=None,status=None):
        res = {}
        
        if(not message is None):
            res['message']['content'] = message
        if(not options is None):
            res['message']['options'] = options
        if(not status is None):
            res['message']['status'] = status
        if(not statuscode is None):
            res['code'] = statuscode
            
        return res
        

class AuthRegister(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, type=str, location="args")
        parser.add_argument('password', required=True, type=str, location="args")
        args = parser.parse_args()
        
        user = User()
        message = user.create_user(args['username'],args['password'])
        return message , message['code']

class AuthLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, type=str, location="args")
        parser.add_argument('password', required=True, type=str, location="args")
        args = parser.parse_args()
        
        user = User()
        res = user.user_login(args['username'],args['password'])
        if res:
            return {'message': res,
            'code': 200},200
        else:
            return {'message': {
                'status': 'failed',
                'content': 'Login Failed. Incorrect username or password'
            },
            'code': 200}


class TaskList(Resource):
    def get(self):

        headers = request.headers.get('Content-Type')
        test = request.form.get('test')
        authorization = request.headers.get('Authorization')

        user_id = Auth(request).validate()
        task = Task(user_id)
        tasklist = []
        for item in task.get_tasks():
            tasklist.append({'id': item[0], 'task': item[1], 'test': test})


        return {
        "test":"test message", 
        "tasks": tasklist
         } , 200

class TaskView(Resource):
    pass

