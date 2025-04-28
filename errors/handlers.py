from flask import jsonify
from utils.response_wrapper import error_response


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return error_response("Resource not found", 404)

    @app.errorhandler(500)
    def internal_error(error):
        return error_response("Internal server error", 500)

    @app.errorhandler(Exception)
    def unhandled_exception(error):
        return error_response("Unexpected error", 500)