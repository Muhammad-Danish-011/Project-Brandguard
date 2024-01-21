# How to Run

To run your Flask application with the specified configuration, follow these steps:

1. Set the environment variables:

    ```bash
    export SECRET_KEY="secretkey"
    export DATABASE_URI="postgresql://postgres:postgres@localhost:5432/brandguard"
    export FLASK_APP=app
    export FLASK_ENV=development
    ```

    Make sure to replace `"secretkey"` with your actual secret key and adjust the `DATABASE_URI` as needed.

2. Run the Flask application:

    ```bash
    flask run
    ```

    This command will start your Flask application in development mode.

# Example Database Initialization

If you need to create the database tables, you can use the Flask shell:

```bash
flask shell

from app.extensions import db
from app.models.models import Post, Question

db.create_all()
