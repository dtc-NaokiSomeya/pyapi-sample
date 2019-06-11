
from typing import Callable, Dict
from os import listdir
from os.path import isfile, join, dirname
from importlib import import_module
from pyapp import exceptions

from flask import Flask, request, jsonify, Request
import inspect
class RequestParser:
    # Authorized user info header, which added by api gateway authorizer
    COGNITO_EMAIL_HEADER = "X-Cognito-Email"
    COGNITO_NAME_HEADER = "X-Cognito-Username"
    COGNITO_OLD_USER_NAME_HEADER = "X-Cognito-Old-Username"

    @classmethod
    def parse(cls) -> Dict:
        req_obj: Request = request
        info = {}
        try:
            # Basic information
            info["httpMethod"]                      = req_obj.method
            info["multiValueHeaders"]               = {}
            for k in req_obj.headers.keys():
                info["multiValueHeaders"][k] = req_obj.headers.get_all(k)
            info["multiValueQueryStringParameters"] = {}
            for k in req_obj.args.keys():
                info["multiValueQueryStringParameters"][k] = req_obj.args.getlist(k)
            info["body"]                            = req_obj.get_json()
            info["isBase64Encoded"]                 = False

            # Auth information
            if len(req_obj.headers.get_all(cls.COGNITO_NAME_HEADER)) != 1 or len(req_obj.headers.get_all(cls.COGNITO_EMAIL_HEADER)) != 1 or len(req_obj.headers.get_all(cls.COGNITO_OLD_USER_NAME_HEADER)) != 1:
                # NOTICE: If authorized user info headers are multiply set, raise unauth error.
                raise exceptions.UnauthorizedError()
            info["cognito:username"]        = req_obj.headers[cls.COGNITO_NAME_HEADER]
            info["email"]                   = req_obj.headers[cls.COGNITO_EMAIL_HEADER]
            info["custom:old_user_name"]    = req_obj.headers[cls.COGNITO_OLD_USER_NAME_HEADER]
            info["path"] = req_obj.path

            info["sourceIp"]                = req_obj.remote_addr
        except KeyError as e:
            raise exceptions.UnauthorizedError()

        return info

class HttpMethods:
    def POST(func: Callable) -> Callable:
        def wrapper(**kwargs):
            req = RequestParser.parse()
            if req["body"] is None or req["httpMethod"] != "POST":
                raise exceptions.InvalidContentType()
            return jsonify(func(req))
        return wrapper

    def GET(func: Callable) -> Callable:
        def wrapper(**kwargs):
            req = RequestParser.parse()
            return jsonify(func(req))
        return wrapper

# Auto routing
def auto_route_loader(app: Flask):
    """
    auto_route_loader
    import rest/* modules and read "callstacks" which define [ subpath, method, function ].
    """
    rest_path = join(dirname(__file__), '.')
    pyfiles = [f for f in listdir(rest_path) if isfile(join(rest_path, f)) and f != "__init__.py"]
    for pyfile in pyfiles:
        resource = pyfile.split(".")[0]
        plugin = import_module(globals()['__name__']+"."+resource)
        for callstack in plugin.callstacks:
            print(callstack)
            app.add_url_rule("/"+resource+"/"+callstack[0], callstack[0]+"_"+resource, callstack[1]((callstack[2])), methods=[callstack[1].__name__])

def auto_register_errorhandle(app: Flask):
    def handle_rest_exception(err: exceptions.BaseRestException):
        response = jsonify(err.to_dict())
        response.status_code = err.status_code
        return response
    # loop exceptions
    for name, obj in inspect.getmembers(exceptions):
        if inspect.isclass(obj):
            app.register_error_handler(obj, handle_rest_exception)

