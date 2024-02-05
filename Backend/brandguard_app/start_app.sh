# start_app.sh

export SECRET_KEY="secretkey"
export DATABASE_URI="postgresql://postgres:123@localhost:5432/brandguard"
export FLASK_APP=app.factory:create_app
export FLASK_ENV=development

flask run
