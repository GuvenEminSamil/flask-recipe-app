from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from authlib.integrations.flask_client import OAuth


db = SQLAlchemy()
session = Session()
oauth = OAuth()

def create_app(config_class="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    session.init_app(app)
    oauth.init_app(app)

    oauth.register(
        name='github',
        client_id=app.config["GITHUB_CLIENT_ID"],
        client_secret=app.config["GITHUB_CLIENT_SECRET"],
        access_token_url='https://github.com/login/oauth/access_token',
        access_token_params=None,
        authorize_url='https://github.com/login/oauth/authorize',
        authorize_params=None,
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'},
    )

    oauth.register(
        name='yandex',
        client_id=app.config["YANDEX_CLIENT_ID"],
        client_secret=app.config["YANDEX_CLIENT_SECRET"],
        access_token_url='https://oauth.yandex.com/token',
        authorize_url='https://oauth.yandex.com/authorize',
        api_base_url='https://login.yandex.ru/info',
        client_kwargs={'scope': 'login:email login:info'}
    )

    with app.app_context():
        from .models import user
        db.create_all()

        from app.views.auth import RegisterView, LoginView, LogoutView, ProfileView, github_login, github_callback, yandex_login, yandex_callback
        from app.views.recipe import RecipeSearchView
        app.add_url_rule("/register", view_func=RegisterView.as_view("register"))
        app.add_url_rule("/login", view_func=LoginView.as_view("login"))
        app.add_url_rule("/logout", view_func=LogoutView.as_view("logout"))
        app.add_url_rule("/profile", view_func=ProfileView.as_view("profile"))
        app.add_url_rule("/login/github", view_func=github_login)
        app.add_url_rule("/login/github/callback", view_func=github_callback)
        app.add_url_rule("/login/yandex", view_func=yandex_login)
        app.add_url_rule("/login/yandex/callback", view_func=yandex_callback)

        app.add_url_rule("/meals", view_func=RecipeSearchView.as_view("meal_search"))

    return app