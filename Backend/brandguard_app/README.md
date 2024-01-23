# How to Run

To run your Flask application with the specified configuration, follow these steps:

### Set Up Environment Variables

Instead of manually setting environment variables each time, you can create a `.env` file in the root directory of your Flask project with the following content:

```plaintext
SECRET_KEY=secretkey
DATABASE_URI=postgresql://postgres:postgres@localhost:5432/brandguard
FLASK_APP=app
FLASK_ENV=development
```

Make sure to replace `secretkey` with your actual secret key and adjust the `DATABASE_URI` as needed.

### Install Required Packages

Ensure all required packages are installed by running:

```bash
pip install -r requirements.txt
```

### Initialize and Migrate Database

Before running the application for the first time, initialize and migrate your database:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

These commands set up the necessary database tables and apply any changes you've made to your models.

### Run the Application

To start the Flask application, use the provided script:

```bash
./start_app.sh
```

This script will automatically load the environment variables from the `.env` file and start your Flask application in development mode.

---

**Additional Notes:**

- Ensure that `python-dotenv` is included in your `requirements.txt` file for automatic loading of environment variables.
- The `start_app.sh` script should contain the command `flask run` and not need to export the environment variables again, as they will be loaded from the `.env` file.
- The `.env` file should be excluded from version control for security reasons (e.g., add `.env` to your `.gitignore` file).
- Make sure your database server is running and accessible before performing the database initialization and migration steps.
- The initial migration command (`flask db migrate -m "Initial migration"`) is only needed once or when there are changes to the database models.