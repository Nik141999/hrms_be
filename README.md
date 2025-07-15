FastAPI Backend Application
===========================

This is a backend API application built using FastAPI and SQLAlchemy.
It supports authentication with python-jose, password hashing with passlib,
and uses Alembic for handling database migrations.

Requirements
------------
- Python 3.8 or higher
- Install dependencies using:

    pip install -r requirements.txt

Run Command
-----------
To start the development server with auto-reload, use the following command:

    python run.py

Make sure your FastAPI app is located in app/main.py and the app instance is named 'app'.
Modify the path if your structure is different.

Accessing API Documentation: How to access the automatically generated OpenAPI/Swagger UI documentation (usually at /docs or /redoc).


Database Setup and Migrations (Alembic):

Initializing Alembic: How to set up Alembic for the first time.

Creating Migrations: Commands to generate new migration scripts when schema changes occur (e.g., alembic revision --autogenerate -m "Description of change").

Applying Migrations: Instructions for upgrading the database to the latest schema version (e.g., alembic upgrade head).

Downgrading Migrations: Commands for reverting migrations if needed (e.g., alembic downgrade -1).