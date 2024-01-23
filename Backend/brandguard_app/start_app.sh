# start_app.sh

export SECRET_KEY="secretkey"
export DATABASE_URI="postgresql://brandguard:brandguard@localhost:5432/brandguard_db"
export FLASK_APP=app
export FLASK_ENV=development

flask run
