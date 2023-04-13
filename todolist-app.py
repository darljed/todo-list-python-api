from flask import Flask
from flask_restful import Resource, Api, reqparse
import ast, jsonify

app = Flask(__name__)
api = Api(app)
print("test")

class Auth(Resource):
    
    def get(self):
        res = {
            'message':'Hey! Im just checking out the response. '
        }
        return {'response': res}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, type=str, location="args")
        parser.add_argument('password', required=True, type=str, location="args")
        args = parser.parse_args()
        return {"username":args['username'], "password":args['password']}, 200 



api.add_resource(Auth,'/auth')

if __name__ == "__main__":
    app.run(debug=True)