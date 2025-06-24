import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:876678asd@localhost:5432/python_project_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'instance', 'flask_session')
    SESSION_PERMANENT = False
    SESSION_COOKIE_NAME = "flask_session"
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False

    GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

    YANDEX_CLIENT_ID = os.getenv("YANDEX_CLIENT_ID")
    YANDEX_CLIENT_SECRET = os.getenv("YANDEX_CLIENT_SECRET")