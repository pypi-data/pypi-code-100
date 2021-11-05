class BadRequest(Exception):
    status_code = 400

class Forbidden(BadRequest):
    status_code = 403

class NotFound(BadRequest):
    status_code = 404

class NotAllowed(BadRequest):
    status_code = 405

class ImATeapot(BadRequest):
    status_code = 418
