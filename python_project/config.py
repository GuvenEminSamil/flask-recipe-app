import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:876678asd@localhost:5432/python_project_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False