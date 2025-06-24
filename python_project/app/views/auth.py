from flask import render_template, redirect, url_for, request, flash, session, abort, current_app
from flask.views import MethodView
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms.auth_forms import ProfileForm
import os

from app import db, oauth
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
            flash("Registration successful. You can now log in.")
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
                flash("Logged in successfully.")
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
        flash("Logged out.")
        return redirect(url_for("login"))




class ProfileView(MethodView):
    def get(self):
        if "user_id" not in session:
            return redirect(url_for("login"))

        user = User.query.get(session["user_id"])
        if not user:
            abort(404)

        form = ProfileForm(obj=user)
        return render_template("auth/profile.html", form=form)

    def post(self):
        if "user_id" not in session:
            return redirect(url_for("login"))

        form = ProfileForm()
        if form.validate_on_submit():
            user = User.query.get(session["user_id"])
            if not user:
                abort(404)

            user.username = form.username.data
            user.email = form.email.data

            if form.password.data:
                user.password_hash = generate_password_hash(form.password.data)

            db.session.commit()
            flash("Profile updated.")
            return redirect(url_for("profile"))

        return render_template("auth/profile.html", form=form)



@current_app.route("/login/github")
def github_login():
    session.permanent = True
    redirect_uri = "http://localhost:5000/login/github/callback"
    print("Session before redirect:", dict(session))
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
        password_hash = generate_password_hash(os.urandom(16).hex()))
        db.session.add(user)
        db.session.commit()

    session["user_id"] = user.id
    session["username"] = user.username
    flash("Logged in with GitHub.", 'success')
    print("Session on callback:", dict(session))
    return redirect(url_for("profile"))


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
                    password_hash=generate_password_hash(os.urandom(16).hex()))
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        session["username"] = user.username
        flash("Logged in with Yandex.", 'success')
        return redirect(url_for("profile"))
    return redirect(url_for("login"))