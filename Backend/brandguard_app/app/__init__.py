import atexit

from app.extensions import db, migrate, scheduler
from app.main import bp as main_bp
from config import Config
from flask import Flask


def create_app(config_class=Config, start_scheduler=True):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints here
    app.register_blueprint(main_bp)

    if start_scheduler:
        # Start the scheduler only if not already started
        if not scheduler.running:
            scheduler.start()
            atexit.register(lambda: scheduler.shutdown())

    return app
