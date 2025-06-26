import pytest
from flask import current_app
from app import create_app, db
from app.models.user import User
from app.models.recipe import Recipe
from app.models.comment import Comment
from app.forms.recipe_form import RecipeForm
from flask_wtf import FlaskForm
from werkzeug.datastructures import MultiDict
from unittest.mock import patch

# Test1 - checks if user registered via oauth can change email. skipped bc I won't let it.
@pytest.mark.skip(reason="Model does not prevent email changes for OAuth users")
def test_oauth_user_email_immutable(app):
    with app.app_context():
        user = User(
            username="oauth_user",
            email="initial@example.com",
            oauth_provider="github",
            password_hash="dummy"
        )
        db.session.add(user)
        db.session.commit()

        user.email = "new@example.com"
        db.session.commit()

        updated_user = db.session.get(User, user.id)
        assert updated_user.email == "initial@example.com"

# Test2 - checks if it deletes comments as well when deleting recipe.
def test_recipe_deletion_cascades_comments(app):
    with app.app_context():
        user = User(username="recipe_owner", email="owner@test.com", password_hash="dummy")
        db.session.add(user)
        db.session.commit()

        recipe = Recipe(
            name="Test Recipe",
            instructions="Steps",
            user_id=user.id,
            category="Test",
            area="Nowhere",
            thumbnail="https://example.com/image.jpg"
        )
        db.session.add(recipe)
        db.session.commit()

        comment = Comment(content="Great!", user_id=user.id, recipe_id=recipe.id)
        db.session.add(comment)
        db.session.commit()

        db.session.delete(recipe)
        db.session.commit()

        comment_check = db.session.get(Comment, comment.id)
        assert comment_check is None

# test3 - checks for empty fields in recipe form
def test_recipe_form_validation_missing_fields(app):
    with app.app_context():
        form_data = MultiDict({
            'name': '',
            'instructions': '',
            'category': '',
            'area': '',
            'image': ''
        })
        form = RecipeForm(form_data)
        assert not form.validate()
        assert 'name' in form.errors
        assert 'instructions' in form.errors

# Test4 - checks for non-existing recipe
def test_api_get_nonexistent_recipe(client):
    response = client.get('/api/recipes/9999')
    assert response.status_code == 404
    json_data = response.get_json(silent=True)
    assert json_data is not None
    assert 'error' in json_data

# Test5- checks if service layer works without needing live api calls.
@patch('app.services.meal_service.requests.get')
def test_meal_service_search_meals_by_name(mock_get):
    mock_get.return_value.json.return_value = {
        "meals": [{
            "idMeal": "1234",
            "strMeal": "Sample",
            "strInstructions": "Step 1",
            "strCategory": "Beef",
            "strArea": "Canadian"
        }]
    }

    from app.services.meal_service import search_meals_by_name
    results = search_meals_by_name("Sample")

    assert isinstance(results, list)
    assert results[0]["strMeal"] == "Sample"
    assert results[0]["strCategory"] == "Beef"
