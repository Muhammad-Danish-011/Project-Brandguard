# start_app.sh

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

export SECRET_KEY="secretkey"
export DATABASE_URI="postgresql://postgres:postgres@localhost:5432/brandguard"
export FLASK_APP=app.factory:create_app
export FLASK_ENV=development

flask run
