
from typing import Callable
from os import listdir
from os.path import isfile, join, dirname
from importlib import import_module
from pyapp import exceptions

from flask import Flask, request, jsonify
import inspect
class HttpMethods:
    def POST(func: Callable) -> Callable:
        def wrapper(**kwargs):
            req_body = request.get_json()
            if req_body is None:
                raise exceptions.InvalidContentType()
            return jsonify(func(req_body))
        return wrapper

    def GET(func: Callable) -> Callable:
        def wrapper(**kwargs):
            get_params = request.args
            return jsonify(func(get_params))
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

