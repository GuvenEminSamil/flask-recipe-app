from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from authlib.integrations.flask_client import OAuth
from flask_socketio import SocketIO


db = SQLAlchemy()
session = Session()
oauth = OAuth()
socketio = SocketIO()

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

    with (app.app_context()):
        from .models import user
        db.create_all()

        from app.views.auth import RegisterView, LoginView, LogoutView, ProfileOverviewView, ProfileEditView, github_login, github_callback, yandex_login, yandex_callback
        from app.views.recipe import RecipeDetailView
        from app.views.home import HomeView
        from app.views.comment import CommentCreateView, CommentEditView, CommentDeleteView
        from app.views.user_recipe import RecipeCreateView, RecipeEditView, RecipeDeleteView
        from app.api.endpoints import api_bp
        from app.websocket.chat import socketio_bp

        app.add_url_rule("/register", view_func=RegisterView.as_view("register"))
        app.add_url_rule("/login", view_func=LoginView.as_view("login"))
        app.add_url_rule("/logout", view_func=LogoutView.as_view("logout"))
        app.add_url_rule("/profile", view_func=ProfileOverviewView.as_view("profile"))
        app.add_url_rule("/profile/edit", view_func=ProfileEditView.as_view("profile_edit"))
        app.add_url_rule("/login/github", view_func=github_login)
        app.add_url_rule("/login/github/callback", view_func=github_callback)
        app.add_url_rule("/login/yandex", view_func=yandex_login)
        app.add_url_rule("/login/yandex/callback", view_func=yandex_callback)

        app.add_url_rule("/meals/<int:meal_id>", view_func=RecipeDetailView.as_view("meal_detail"))

        app.add_url_rule("/", view_func=HomeView.as_view("home"))

        app.add_url_rule("/recipes/<int:recipe_id>/comments", view_func=CommentCreateView.as_view("comment_create"))
        app.add_url_rule("/comments/<int:comment_id>/edit", view_func=CommentEditView.as_view("comment_edit"))
        app.add_url_rule("/comments/<int:comment_id>/delete", view_func=CommentDeleteView.as_view("comment_delete"))

        app.add_url_rule("/recipes/add", view_func=RecipeCreateView.as_view("recipe_create"))
        app.add_url_rule("/recipes/<int:recipe_id>/edit", view_func=RecipeEditView.as_view("recipe_edit"))
        app.add_url_rule("/recipes/<int:recipe_id>/delete", view_func=RecipeDeleteView.as_view("recipe_delete"))

        app.register_blueprint(api_bp)
        app.register_blueprint(socketio_bp)

        socketio.init_app(app)

    return app