from flask import render_template
from app.main import bp


@bp.route('/')
def index():
    return 'Welcome to Brandguard!'

@bp.route('/hello/')
def hello():
    return 'Hello, World!'