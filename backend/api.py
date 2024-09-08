from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)

@api.route('/test')
class TestRoute(Resource):
    def get(self):
        return {'message': 'everything ok'}, 200
    
if __name__ == '__main__':
    app.run(debug=True)