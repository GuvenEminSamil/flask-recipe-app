from flask import render_template, redirect, url_for, session,request
from flask.views import MethodView
from app.models.recipe import Recipe

class HomeView(MethodView):
    def get(self):
        if "user_id" not in session:
            return redirect(url_for("login"))

        page = int(request.args.get("page", 1))
        per_page = 9

        pagination = Recipe.query.order_by(Recipe.name).paginate(page=page, per_page=per_page)
        return render_template("home.html", meals=pagination.items, pagination=pagination)