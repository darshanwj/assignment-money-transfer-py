from flask import Flask


def create_app():
    app = Flask(__name__)

    from .models import ma
    ma.init_app(app)

    from .api.views import bp
    app.register_blueprint(bp)

    return app
