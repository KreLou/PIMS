import os
from flask import Flask
from . import db
from . import test

def create_app():
    app = Flask(__name__)

    db.init_app(app)

    app.register_blueprint(test.bp)

    return app
