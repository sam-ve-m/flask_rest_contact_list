from flask import Flask
from flask_pydantic_spec import FlaskPydanticSpec
from flask_restful import Api

from src.routes.resources import ContactResource

app = Flask(__name__)
api = Api(app)
contract_specification = FlaskPydanticSpec("study", title="Some title")
contract_specification.register(app)
api.add_resource(ContactResource, '/contact')

if __name__ == '__main__':
    app.run(
        host='localhost',
        port='4444',
        debug=True
    )
