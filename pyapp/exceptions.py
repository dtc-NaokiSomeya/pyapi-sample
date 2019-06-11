
class BaseRestException(Exception):
    def __init__(self, message="", payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = -1 # must set on inherited class
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class InvalidContentType(BaseRestException):
    def __init__(self):
        BaseRestException.__init__(self)
        self.status_code = 400
        self.message = "Invalid Content-Type"

class UnauthorizedError(BaseRestException):
    def __init__(self):
        BaseRestException.__init__(self)
        self.status_code = 401
        self.message = "Unauthorized"