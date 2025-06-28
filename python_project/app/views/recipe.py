from flask import render_template
from flask.views import MethodView
from app.services.meal_service import get_meal_by_id
from app.models.recipe import Recipe
from app.models.user import User
from app import db
from flask import session
from app.forms.comment_form import CommentForm


class RecipeDetailView(MethodView):
    def get(self, meal_id):
        recipe = Recipe.query.get(meal_id)
        if not recipe:
            data = get_meal_by_id(meal_id)
            if not data:
                return render_template("recipes/not_found.html"), 404

            recipe = Recipe(
                id=int(data["idMeal"]),
                name=data["strMeal"],
                category=data["strCategory"],
                area=data["strArea"],
                instructions=data["strInstructions"],
                thumbnail=data["strMealThumb"],
            )
            db.session.add(recipe)
            db.session.commit()

        user = User.query.get(session.get("user_id"))

        form = CommentForm()

        return render_template("recipes/detail.html", recipe=recipe, user=user, form=form, User=user)