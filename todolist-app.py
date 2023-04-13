from flask import Flask
from flask_restful import Resource, Api, reqparse
from config import AUTH_URLS, TASK_URLS
from controller import User

app = Flask(__name__)
api = Api(app)


class AuthRegister(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, type=str, location="args")
        parser.add_argument('password', required=True, type=str, location="args")
        args = parser.parse_args()
        
        user = User()
        message = user.create_user(args['username'],args['password'])
        return {'message': message,'code': 200} , 200

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


# ENDPOINTS

api.add_resource(AuthRegister,AUTH_URLS['AuthRegister'])
api.add_resource(AuthLogin,AUTH_URLS['AuthLogin'])

# ERROR HANDLERS
@app.errorhandler(404) 
def invalid_route(e): 
    return {'message': 'Invalid route.', 'code': 404} , 404

@app.errorhandler(500) 
def invalid_route(e): 
    return {'message': 'Internal Server Error','code': 500} , 500

if __name__ == "__main__":
    app.run(debug=True)