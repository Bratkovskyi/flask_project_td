from flask import jsonify
from flask_limiter import RateLimitExceeded

from utils.response_wrapper import error_response


def register_error_handlers(app):

    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit(error):
        print(RateLimitExceeded)
        return error_response("Too many requests. Please try again later", 429)

    @app.errorhandler(404)
    def not_found(error):
        return error_response("Resource not found", 404)

    @app.errorhandler(500)
    def internal_error(error):
        return error_response("Internal server error", 500)

    @app.errorhandler(Exception)
    def unhandled_exception(error):
        return error_response("Unexpected error", 500)