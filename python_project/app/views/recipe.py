from flask import request, render_template
from flask.views import MethodView
from app.services.meal_service import search_meals_by_name

class RecipeSearchView(MethodView):
    def get(self):
        query = request.args.get("q", "")
        meals = search_meals_by_name(query) if query else[]
        return render_template("recipes/search.html", meals=meals, query=query)
