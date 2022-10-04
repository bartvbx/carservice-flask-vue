from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from .config import Config

db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    CORS(app, resources={r"/*": {'origins': "*"}})
    db.init_app(app)
    ma.init_app(app)
    
    with app.app_context():
        from carservice.views.parts import parts_bp
        # from carservice.views.services import services_bp
        from carservice.views.clients import clients_bp
        # from carservice.views.visits import visits_bp

        app.register_blueprint(parts_bp)
        # app.register_blueprint(services_bp)
        app.register_blueprint(clients_bp)
        # app.register_blueprint(visits_bp)

        from .models import Part, Client

        db.create_all()
        db.session.commit()

        return app
