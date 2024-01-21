How to Run:

export SECRET_KEY="secretkey"
export DATABASE_URI="postgresql://postgres:postgres@localhost:5432/brandguard"
export FLASK_APP=app
export FLASK_ENV=development
flask run


Example DB:
flask shell

from app.extensions import db
from app.models.models import Post, Question
db.create_all()