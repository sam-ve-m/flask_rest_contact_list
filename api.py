from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class RestResource1(Resource):
    def get(self, some_item: int):
        return {'hello': 'world ' + str(some_item)}


class RestResource2(Resource):
    def get(self, some_item: int):
        return {'hello': 'world ' + str(some_item)}


class RestResource3(Resource):
    def get(self, some_item: int):
        return {'hello': 'world ' + str(some_item)}


api.add_resource(RestResource1, '/rte', '/resource1/<int:some_item>')
api.add_resource(RestResource2, '/rte', '/resource2/<int:some_item>')
api.add_resource(RestResource3, '/rte', '/resource3/<int:some_item>')


if __name__ == '__main__':
    app.run(
        host='localhost',
        port='4444',
        debug=True
    )
