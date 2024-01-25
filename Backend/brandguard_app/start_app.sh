# start_app.sh

export SECRET_KEY="secretkey"
export DATABASE_URI="postgresql://postgres:postgres@localhost:5432/brandguard"
export FLASK_APP=app
export FLASK_ENV=development

flask run
