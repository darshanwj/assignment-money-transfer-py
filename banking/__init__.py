import os
from flask import Flask
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_mapping(
    _DATABASE=os.path.join(app.instance_path, 'banking.sqlite3'),
    _CURRENCIES=['USD', 'AED', 'GBP']
)

ma = Marshmallow()
ma.init_app(app)

from . import views  # noqa
