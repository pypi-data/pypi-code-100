def clean_locals(kwargs: dict):
    return {key: value for key, value in kwargs.items() if not key.startswith("_") and key != "self"}
