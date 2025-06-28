from flask import render_template, redirect, url_for, session,request
from flask.views import MethodView
from sqlalchemy.sql.expression import null

from app.models.recipe import Recipe

class HomeView(MethodView):
    def get(self):
        if "user_id" not in session:
            return redirect(url_for("login"))

        page = int(request.args.get("page", 1))
        per_page = 9
        query = request.args.get("q", "").strip()

        recipe_query = Recipe.query
        if query:
            recipe_query = recipe_query.filter(Recipe.name.ilike(f"%{query}%"))
            if recipe_query.count() == 0:
                return render_template("recipes/not_found.html")

        pagination = recipe_query.order_by(Recipe.name).paginate(page=page, per_page=per_page)
        return render_template("home.html", meals=pagination.items, pagination=pagination, query=query)