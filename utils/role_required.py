from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from utils.response_wrapper import error_response


def role_required(required_roles):
    """
    Checks if the user has the required role or one of the allowed roles.

    :param required_roles: str or list[str]
        A single role as a string or a list of allowed roles.
    """
    if isinstance(required_roles, str):
        required_role = [required_roles]

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("role")

            if user_role not in required_role:
                return error_response("Forbidden: insufficient rights", 403)

            return fn(*args, **kwargs)
        return wrapper
    return decorator
