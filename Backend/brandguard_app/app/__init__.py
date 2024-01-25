from flask import Flask
from config import Config
from app.extensions import db, migrate,scheduler
from app.main import bp as main_bp
import atexit

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    migrate.init_app(app,db)

    # Register blueprints here
    app.register_blueprint(main_bp)

    # Start the scheduler
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

    return app
