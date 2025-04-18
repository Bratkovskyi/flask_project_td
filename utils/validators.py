def validate_task_input(data):
    if not data:
        return "No data provided"
    if "title" not in data:
        return "'title' field is required"
    if not isinstance(data["title"], str):
        return "'title' must be a string"
    if len(data["title"].strip()) == 0:
        return "'title' cannot be empty"
    return None
