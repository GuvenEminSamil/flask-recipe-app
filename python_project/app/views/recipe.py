from flask import request, render_template
from flask.views import MethodView
from app.services.meal_service import search_meals_by_name, get_meal_by_id
from app.models.recipe import Recipe
from app import db

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
        return render_template("recipes/detail.html", recipe=recipe)