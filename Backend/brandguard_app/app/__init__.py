from flask import Flask
from config import Config
from app.extensions import db, migrate,scheduler
from app.main import bp as main_bp
import atexit

def create_app(config_class=Config, start_scheduler=True):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # Set the BASE_UPLOAD_FOLDER configuration option
    BASE_UPLOAD_FOLDER = '/home/muhammadmoizkhan/Music/flask_app/schedular_check/brandguard_app/refrence_images'
    app.config['BASE_UPLOAD_FOLDER'] = BASE_UPLOAD_FOLDER


    # Initialize Flask extensions here
    db.init_app(app)
    migrate.init_app(app,db)

    # Register blueprints here
    app.register_blueprint(main_bp)

    if start_scheduler:
        # Start the scheduler only if not already started
        if not scheduler.running:
            scheduler.start()
            atexit.register(lambda: scheduler.shutdown())

    return app
