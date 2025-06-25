from flask import Blueprint, request, jsonify, session
from flask.views import MethodView
from app.models import Recipe, User, Comment
from app import db

api_bp = Blueprint('api', __name__, url_prefix='/api')

class RecipeListAPI(MethodView):
    def get(self):
        query = request.args.get("q", "").strip()
        recipes_query = Recipe.query

        if query:
            recipes_query = recipes_query.filter(Recipe.name.ilike(f"%{query}%"))

        recipes = recipes_query.all()
        return jsonify([
            {
                "id": recipe.id,
                "name": recipe.name,
                "category": recipe.category,
                "area": recipe.area,
                "thumbnail": recipe.thumbnail,
            } for recipe in recipes
        ])

class UserDetailAPI(MethodView):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email if not user.oauth_provider else None,
            "recipes": [
                {
                    "id": recipe.id,
                    "name": recipe.name,
                } for recipe in user.recipes
            ]
        })

class CommentCreateAPI(MethodView):
    def post(self):
        if "user_id" not in session:
            return jsonify({"error": "Authentication required"}), 401

        data = request.get_json()
        content = data.get("content")
        recipe_id = data.get("recipe_id")

        if not content or recipe_id:
            return jsonify({"error": "Missing required fields"}), 401

        comment = Comment(
            content=content,
            user_id=session["user_id"],
            recipe_id=recipe_id
        )
        db.session.add(comment)
        db.session.commit()

        return jsonify({
            "id": comment.id,
            "content": comment.content,
            "user_id": comment.user_id,
            "recipe_id": comment.recipe_id
        }), 201


api_bp.add_url_rule("/recipes", view_func=RecipeListAPI.as_view("recipes"))
api_bp.add_url_rule("/users/<int:user_id>", view_func=UserDetailAPI.as_view("user_detail"))
api_bp.add_url_rule("/comments", view_func=CommentCreateAPI.as_view("create_comment"))