from flask import Flask
from API import db, values
from API.controller import user, package, address


def create_app():
    app = Flask(__name__)

    db.init_app(app)

    with app.app_context():
        db.init_db()

    app.register_blueprint(values.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(package.bp)
    app.register_blueprint(address.bp)
    return app
