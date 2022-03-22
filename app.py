from flask import Flask
from flask_pydantic_spec import FlaskPydanticSpec
from flask_restful import Api
from flask_cors import CORS

from src.routes.resources import ContactRegisterResource, ContactGetOneResource, ContactGetAllResource, \
    ContactGetAllByLetterResource, ContactUpdateResource, ContactSoftDeleteResource, PhonesCountResource

app = Flask(__name__)
CORS(app)

contract_specification = FlaskPydanticSpec("study", title="Some title")
contract_specification.register(app)

api = Api(app)
api.add_resource(PhonesCountResource, '/count')
api.add_resource(ContactGetAllResource, '/contacts')
api.add_resource(ContactRegisterResource, '/register')
api.add_resource(ContactUpdateResource, '/edit/<string:contact_id>')
api.add_resource(ContactGetOneResource, '/contact/<string:contact_id>')
api.add_resource(ContactSoftDeleteResource, '/remove/<string:contact_id>')
api.add_resource(ContactGetAllByLetterResource, '/contacts/<string:initial_letter>')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port='4444',
        debug=True
    )
