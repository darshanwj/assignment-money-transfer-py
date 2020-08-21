import os
from flask import Flask
from flask_marshmallow import Marshmallow

ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'banking.sqlite3')
    )

    ma.init_app(app)

    from . import db
    db.init_app(app)

    from .api.views import bp
    app.register_blueprint(bp)

    return app
