#!/usr/bin/env python
import logging

from flask import Flask

from server_lib.db_layer_lib.database import db
from server_lib.end_points.sensors_end_point import sensors_endpoint

logging.root.setLevel(level=logging.INFO)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


def setup_database(app):
    with app.app_context():
        db.init_app(app)
        db.drop_all()
        db.create_all()


def main():
    app = create_app()
    setup_database(app)
    app.register_blueprint(sensors_endpoint)
    app.run()


if __name__ == '__main__':
    main()
