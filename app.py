from flask import Flask, jsonify, request
import pg8000

from pyapp.rest import auto_route_loader, auto_register_errorhandle

app = Flask(__name__)
if app.env == "development":
    from flask_cors import CORS
    CORS(app)

VERSION=0.2

# auto routing
auto_route_loader(app)
# auto register errorhandles
auto_register_errorhandle(app)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")