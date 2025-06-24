from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

db = SQLAlchemy()
session = Session()

def create_app(config_class="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    session.init_app(app)

    with app.app_context():
        from .models import user
        db.create_all()

        from app.views.auth import RegisterView, LoginView, LogoutView, ProfileView
        app.add_url_rule("/register", view_func=RegisterView.as_view("register"))
        app.add_url_rule("/login", view_func=LoginView.as_view("login"))
        app.add_url_rule("/logout", view_func=LogoutView.as_view("logout"))
        app.add_url_rule("/profile", view_func=ProfileView.as_view("profile"))

    return app