import json
from typing import Type

from fastapi.encoders import jsonable_encoder
from pydantic import error_wrappers, BaseModel


def valid_schema_data_or_error(raw_data: dict, schema_model: Type[BaseModel]):
    data = {}
    errors = []
    error_str = None
    try:
        cleaned_data = schema_model(**raw_data)
        data = jsonable_encoder(cleaned_data)
    except error_wrappers.ValidationError as e:
        error_str = e.json()
    if error_str is not None:
        try:
            errors = json.loads(error_str)
        except ValueError:
            errors = [{"loc": "non_field_error", "msg": "Unknown error"}]
    return data, errors
