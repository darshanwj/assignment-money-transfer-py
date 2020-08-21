from flask import Flask
from flask_marshmallow import Marshmallow

# Globally accessible libraries
ma = Marshmallow()


def create_app():
    app = Flask(__name__)

    ma.init_app(app)

    from .api.views import bp
    app.register_blueprint(bp)

    return app
