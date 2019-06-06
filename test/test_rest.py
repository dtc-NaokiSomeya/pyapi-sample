from pyapp.rest import auto_route_loader
from flask import Flask
import unittest

class TestRest(unittest.TestCase):

    def test_01_rest(self):
        app = Flask(__name__)
        auto_route_loader(app)
