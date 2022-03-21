from typing import Optional

from flask import Flask, request
from flask_pydantic_spec import FlaskPydanticSpec
from flask_restful import Resource, Api, reqparse, marshal_with, fields
from pydantic import BaseModel

app = Flask(__name__)
api = Api(app)
contract_specification = FlaskPydanticSpec("study", title="Some title")
contract_specification.register(app)


class ExpectedJson(BaseModel):
    hello: int
    name: str
    other: Optional[str]


database = {}


class RequestJsonBodyParser(reqparse.RequestParser):
    def __init__(self, validation_model: BaseModel):
        super().__init__(bundle_errors=True)
        for key, value_type in validation_model.__annotations__.items():
            self.add_argument(
                key,
                nullable=False,
                type=value_type,
                location=("json",),
                required='Optional' not in str(value_type),
            )


class RestResource1(Resource):
    def get(self, some_item: int):
        arguments = RequestJsonBodyParser(ExpectedJson).parse_args()
        return database.get(some_item, {})

    def post(self, some_item: int, **kwargs):
        some_item_body = request.get_json()
        arguments = RequestJsonBodyParser(ExpectedJson).parse_args()
        database.update({
            some_item: some_item_body
        })
        return {x: y for x, y in some_item_body.items()}


api.add_resource(RestResource1, '/rte/resource1/<int:some_item>')

if __name__ == '__main__':
    app.run(
        host='localhost',
        port='4444',
        debug=True
    )
