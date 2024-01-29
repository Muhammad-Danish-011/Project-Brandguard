from flask import Flask
from app.extensions import db, migrate, scheduler
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from app.main import bp as main_bp
        app.register_blueprint(main_bp)

    return app