from typing import Type, Any, Callable
from flask_restful import reqparse, abort
from pydantic import BaseModel, ValidationError


class JsonField(reqparse.Argument):

    def __init__(self, field_name: str, value_type: type, required: bool):
        super().__init__(
            field_name,
            nullable=False,
            type=self._check_value_type(value_type),
            location=("values",),
            required=required,
        )

    def source(self, request):
        return request.get_json()

    @staticmethod
    def _check_value_type(value_type: type) -> Callable[[Any], Any]:
        def check_it(value: Any) -> Any:
            if not isinstance(value, value_type):
                raise ValueError(f"Value {value} not formatted as {value_type}")
            return value
        return check_it


class JsonBodyRequestParser(reqparse.RequestParser):
    def __init__(self, validation_model: Type[BaseModel], all_fields_required: bool = True):
        super().__init__(bundle_errors=True)
        self.validation_model = validation_model
        parse_value_type_methods = {
            'builtins': lambda x: x,
            'typing': lambda x: self._parse_typing_type(x)
        }
        for field, value_type in validation_model.__annotations__.items():
            origin_module = value_type.__module__
            parse_method = parse_value_type_methods.get(origin_module)
            parsed_value_type = parse_method(value_type)
            json_field = JsonField(field, parsed_value_type, all_fields_required)
            self.add_argument(json_field)

    def parse_args(self, req=None, strict=False, http_error_code=400) -> BaseModel:
        parsed_args = super().parse_args(req, strict, http_error_code)
        try:
            return self.validation_model(**parsed_args)
        except ValidationError as error:
            raw_errors = error.errors()
            errors = self._remove_context_values_from_error_messages(raw_errors)
            abort(http_error_code, message={"errors": errors})

    @staticmethod
    def _remove_context_values_from_error_messages(errors: list) -> list:
        for error in errors:
            if error.get("ctx"):
                del error["ctx"]
        return errors

    @staticmethod
    def _parse_typing_type(typing_type) -> type:
        root_type = typing_type.__args__[0]
        return root_type if root_type.__module__ == "builtins" else root_type.__origin__