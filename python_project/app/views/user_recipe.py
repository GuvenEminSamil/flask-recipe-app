from flask import render_template, redirect, url_for, session, flash, abort, current_app
from flask.views import MethodView

from app.models import User
from app.models.recipe import Recipe
from app.forms.recipe_form import RecipeForm
from app import db
import os
from werkzeug.utils import secure_filename

class RecipeCreateView(MethodView):
    def get(self):
        if "user_id" not in session:
            return redirect(url_for("login"))

        form = RecipeForm()
        user = User.query.get(session.get("user_id"))
        return render_template("recipes/create.html", form=form, User=user, user=user)

    def post(self):
        if "user_id" not in session:
            return redirect(url_for("login"))

        form = RecipeForm()
        if form.validate_on_submit():
            filename = None
            if form.image.data:
                filename = secure_filename(form.image.data.filename)
                upload_path = os.path.join(current_app.root_path, "static", "uploads", filename)
                form.image.data.save(upload_path)

            recipe = Recipe(
                name=form.name.data,
                category=form.category.data,
                area=form.area.data,
                instructions=form.instructions.data,
                thumbnail=filename,
                user_id=session["user_id"]
            )
            db.session.add(recipe)
            db.session.commit()
            flash("Recipe Added", "success")
            return redirect(url_for("home"))
        return render_template("recipes/create.html", form=form)


class RecipeEditView(MethodView):
    def get(self, recipe_id):
        recipe = Recipe.query.get_or_404(recipe_id)
        if recipe.user_id != session.get("user_id"):
            abort(403)
        form = RecipeForm(obj=recipe)
        user = User.query.get(session.get("user_id"))
        return render_template("recipes/edit.html", form=form, recipe=recipe, User=user, user=user)

    def post(self, recipe_id):
        recipe = Recipe.query.get_or_404(recipe_id)
        if recipe.user_id != session.get("user_id"):
            abort(403)
        form = RecipeForm()
        if form.validate_on_submit():
            recipe.name = form.name.data
            recipe.category = form.category.data
            recipe.area = form.area.data
            recipe.instructions = form.instructions.data
            if form.image.data:
                filename = secure_filename(form.image.data.filename)
                upload_path = os.path.join(current_app.root_path, "static", "uploads", filename)
                form.image.data.save(upload_path)
                recipe.thumbnail = filename

            db.session.commit()
            flash("Recipe updated.", "success")
            return redirect(url_for("meal_detail", meal_id=recipe.id))
        return render_template("recipes/edit.html", form=form, recipe=recipe)

class RecipeDeleteView(MethodView):
    def post(self, recipe_id):
        recipe = Recipe.query.get_or_404(recipe_id)
        if recipe.user_id != session.get("user_id"):
            abort(403)
        db.session.delete(recipe)
        db.session.commit()
        flash("Recipe deleted.", "info")
        return redirect(url_for("home"))