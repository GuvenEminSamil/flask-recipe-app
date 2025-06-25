import requests
from app import create_app, db
from app.models.recipe import Recipe
import time

app = create_app()

def fetch_all_meals():
    meals = []
    for i in "abcdefghijklmnopqrstuvwxyz":
        try:
            response = requests.get("https://www.themealdb.com/api/json/v1/1/search.php", params={"s": i}, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["meals"]:
                meals.extend(data["meals"])
            time.sleep(1)
        except requests.RequestException as e:
            print(f"Error fetching meals for letter '{i}': {e}")
    return meals

def populate():
    with app.app_context():
        meals = fetch_all_meals()

        for m in meals:
            if Recipe.query.get(m["idMeal"]):
                continue

            recipe = Recipe(
                id=int(m["idMeal"]),
                name=m["strMeal"],
                category=m["strCategory"],
                area=m["strArea"],
                instructions=m["strInstructions"],
                thumbnail=m["strMealThumb"],
            )
            db.session.add(recipe)
            db.session.commit()
            print(f"Imported {len(meals)} meals.")


if __name__ == "__main__":
    populate()