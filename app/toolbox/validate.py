from flask import jsonify, request, abort
from functools import wraps
from jsonschema import Draft4Validator


def validate_schema(schema):
    """Decorator that performs schema validation on the JSON post data in
    the request and returns an error response if validation fails.  It
    calls the decorated function if validation succeeds.
    :param schema: Schema that represents the expected input.
    """
    validator = Draft4Validator(schema)

    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            input = request.get_json(force=True)
            errors = [error.message for error in validator.iter_errors(input)]
            if errors:
                response = jsonify(dict(success=False,
                                        message="invalid input",
                                        errors=errors))
                response.status_code = 406
                return response
            else:
                return fn(*args, **kwargs)
        return wrapped
    return wrapper
