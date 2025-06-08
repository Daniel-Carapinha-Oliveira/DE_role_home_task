# Home Task Django App

This is the **Home Task** Django application. This README will help you get up and running, including how to install
dependencies, configure the project, and run the test suite using `pytest`.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation and setup](#installation-and-setup)
3. [Running the Development Server](#running-the-development-server)
4. [Running Tests](#running-tests)
5. [Extending the project](#extending-the-project)

---

## Prerequisites

1. **To run with a virtual environment**

- **Python 3.12**
- **pip** (usually bundled with Python)
- **virtualenv** or **venv** (highly recommended)

2. **To run with docker:**

- **Docker desktop**

---

## Installation and setup

1. **Clone the repository.**

2. **Setup secret key:**
    - **Remove `.example` from the file `.env.example` in the root of the project.**
    - **Generate new secret key:**
        - Activate your virtual environment, navigate to the project’s root directory, and run the following commands:
            - python manage.py shell
            - from django.core.management.utils import get_random_secret_key
            - print(get_random_secret_key())
        - Copy the secret key and paste it after `SECRET_KEY=`

---

## Running the Development Server

1. **Run the development server with python:**
    - **Install project dependencies (files in requirements folder):**
        - **Project:**
            - **pip install -r base.txt**
        - **Project and tests:**
            - **pip install -r tests.txt**

- python manage.py runserver
- After running, the project will be available at: http://localhost:8000

2. **To run the project with docker, simply use the following command in Windows CMD:**

- **docker-compose build && docker-compose up -d**
- After running, the project will be available at: http://localhost:8001

---

## Running tests

1. **All tests:**

- pytest

2. **Specific test file (in this example test_models.py for the customers app):**

- pytest apps/customers/tests/test_models.py

3. **Specific class:**

- pytest apps/customers/tests/test_models.py::TestCustomerModel

4. **Specific test:**

- pytest apps/customers/tests/test_models.py::TestCustomerModel::test_first_name_max_length

---

## Extending the project

1. **In case you want to extend this project and change the type of database, you must:**
    - Modify your Django project's `settings.py` to update the DATABASES setting with the new database engine and
      connection parameters.
    - Review your models to ensure the field types are appropriate and compatible with the new database engine, as some
      data types or constraints may behave differently depending on the engine.
    - Delete the old `migrations/` for each app, and run `python manage.py makemigrations` and
      `python manage.py migrate`. Django will generate migration files appropriate for your new engine.
    - If you want to preserve existing data from data.db, find a suitable method to migrate that data to the new
      database.
    - You must update the docker files to reflect this database change.
    - Use the existing .env logic to manage database credentials and secrets securely.