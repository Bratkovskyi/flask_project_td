from flask import jsonify


def success_response(data=None, status=200):
    """
    Returns a standardized success JSON response.

    :param data: Any serializable data (dict, list, etc.)
    :param status: HTTP status code (default: 200)
    :return: Flask Response with JSON
    """
    return jsonify({
        "success": True,
        "data": data
    }), status


def error_response(message="Unknown error", status=400):
    """
    Returns a standardized error JSON response.

    :param message: String or dict with error details
    :param status: HTTP status code (default: 400)
    :return: Flask Response with JSON
    """
    return jsonify({
        "success": False,
        "error": message
    }), status
