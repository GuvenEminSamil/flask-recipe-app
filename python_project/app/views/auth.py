from flask import render_template, redirect, url_for, request, flash, session, abort, current_app
from flask.views import MethodView
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms.auth_forms import ProfileForm
import os
from app.forms.preferences_form import PreferencesForm

from app import db, oauth
from app.models import Recipe
from app.models.preferences import UserPreferences
from app.models.user import User
from app.forms.auth_forms import RegisterForm, LoginForm


class RegisterView(MethodView):
    def get(self):
        form = RegisterForm()
        return render_template("auth/register.html", form=form)

    def post(self):
        form = RegisterForm()
        if form.validate_on_submit():

            if User.query.filter_by(username=form.username.data).first():
                flash("Username already exists.")
                return render_template("auth/register.html", form=form)

            user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data)
            )
            db.session.add(user)
            db.session.commit()
            flash("Registration successful. You can now log in.", "success")
            return redirect(url_for("login"))
        return render_template("auth/register.html", form=form)




class LoginView(MethodView):
    def get(self):
        form = LoginForm()
        return render_template("auth/login.html", form=form)

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password_hash, form.password.data):
                session["user_id"] = user.id
                session["username"] = user.username
                flash("Logged in successfully.", "success")
                if not user.preferences:
                    from app.models.preferences import UserPreferences
                    user.preferences = UserPreferences()
                    db.session.commit()

                return redirect(url_for("profile"))
            else:
                flash("Invalid email or password.", "danger")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{getattr(form, field).label.text}: {error}", "danger")
        return render_template("auth/login.html", form=form)




class LogoutView(MethodView):
    def get(self):
        session.clear()
        flash("Logged out.", "success")
        return redirect(url_for("login"))




class ProfileEditView(MethodView):
    def get(self):
        if "user_id" not in session:
            return redirect(url_for("login"))

        user = User.query.get(session["user_id"])

        if not user:
            abort(404)

        form = ProfileForm(obj=user)
        if user.oauth_provider:
            del form.email
            del form.username
            del form.password
            return render_template("auth/no_access.html", form=form)
        return render_template("auth/profile_edit.html", form=form)

    def post(self):
        if "user_id" not in session:
            return redirect(url_for("login"))

        form = ProfileForm(request.form)
        if form.validate_on_submit():
            user = User.query.get(session["user_id"])

            if user.oauth_provider:
                del form.email

            if not user:
                abort(404)

            user.username = form.username.data
            user.email = form.email.data

            if form.password.data:
                user.password_hash = generate_password_hash(form.password.data)

            db.session.commit()
            session["username"] = user.username
            session["email"] = user.email

            flash("Profile updated.", "success")
            return redirect(url_for("profile"))

        return render_template("auth/profile_edit.html", form=form)

class ProfileOverviewView(MethodView):
    def get(self):
        if "user_id" not in session:
            return redirect(url_for("login"))

        user = User.query.get(session["user_id"])
        if not user:
            abort(404)

        favorite_meals = user.favorites
        user_recipes = user.recipes

        return render_template("auth/profile.html", user=user, favorites=favorite_meals, user_recipes=user_recipes)

class PreferencesView(MethodView):
    def get(self):
        user = User.query.get(session["user_id"])
        if not user.preferences:
            user.preferences = UserPreferences()
            db.session.commit()
        form = PreferencesForm(obj=user.preferences)
        return render_template("auth/preferences.html", form=form)

    def post(self):
        user = User.query.get(session["user_id"])
        form = PreferencesForm()
        if form.validate_on_submit():
            user.preferences.dark_mode = form.dark_mode.data
            db.session.commit()
            flash("Preferences updated", "success")
        return redirect(url_for("home"))


@current_app.route("/login/github")
def github_login():
    session.permanent = True
    redirect_uri = "http://localhost:5000/login/github/callback"
    return oauth.github.authorize_redirect(redirect_uri)

@current_app.route("/login/github/callback")
def github_callback():
    token = oauth.github.authorize_access_token()
    resp = oauth.github.get("user", token=token)
    profile = resp.json()

    github_email = profile.get("email") or profile.get("login") + "@github.com"
    user = User.query.filter_by(email=github_email).first()

    if not user:
        user = User(username=profile.get("login"), email=github_email,
        password_hash = generate_password_hash(os.urandom(16).hex()),
                    oauth_provider="github")
        db.session.add(user)
        db.session.commit()

    session["user_id"] = user.id
    session["username"] = user.username
    flash("Logged in with GitHub.", 'success')
    return redirect(url_for("home"))


@current_app.route("/login/yandex")
def yandex_login():
    session.permanent = True
    redirect_uri = "http://localhost:5000/login/yandex/callback"
    return oauth.yandex.authorize_redirect(redirect_uri)

@current_app.route("/login/yandex/callback")
def yandex_callback():
    token = oauth.yandex.authorize_access_token()
    resp = oauth.yandex.get("", token=token)
    profile = resp.json()

    email = profile.get("default_email") or profile.get("email") or f"{profile['login']}@yandex.com"
    username = profile.get("real_name") or profile.get("login")

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(username=username, email=email,
                    password_hash=generate_password_hash(os.urandom(16).hex()),
                    oauth_provider="yandex")
        db.session.add(user)
        db.session.commit()

    session["user_id"] = user.id
    session["username"] = user.username
    flash("Logged in with Yandex.", 'success')
    return redirect(url_for("home"))

@current_app.route("/favorite/<int:recipe_id>", methods=["POST"])
def toggle_favorite(recipe_id):
    if "user_id" not in session:
        flash("Login required to favorite meals", "warning")
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    recipe = Recipe.query.get(recipe_id)

    if not recipe:
        flash("Recipe not found", "danger")
        return redirect(url_for("home"))

    if recipe in user.favorites:
        user.favorites.remove(recipe)
        flash("Removed from favorites.", "info")
    else:
        user.favorites.append(recipe)
        flash("Added to favorites.", "success")

    db.session.commit()
    return redirect(request.referrer or url_for("home"))