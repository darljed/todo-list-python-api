from flask import Flask
from flask_restful import Api
from config import AUTH_URLS, TASK_URLS
import controller


app = Flask(__name__)
api = Api(app)

# ERROR HANDLERS
@app.errorhandler(404) 
def invalid_route(e): 
    return {'message': 'Invalid route.', 'code': 404} , 404


# ENDPOINTS
api.add_resource(controller.AuthRegister,AUTH_URLS['AuthRegister'])
api.add_resource(controller.AuthLogin,AUTH_URLS['AuthLogin'])

# AUTH NEEDED ENDPOINTS 
api.add_resource(controller.TaskList,TASK_URLS['TaskList'])


if __name__ == "__main__":
    app.run(debug=True)