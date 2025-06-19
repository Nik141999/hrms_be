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

