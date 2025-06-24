import requests

API_BASE = "https://www.themealdb.com/api/json/v1/1"

def search_meals_by_name(name):
    response = requests.get(f"{API_BASE}/search.php", params={"s": name})
    return response.json().get("meals", [])

def get_meal_by_id(meal_id):
    response = requests.get(f"{API_BASE}/lookup.php", params={"i": meal_id})
    meals = response.json().get("meals",[])
    return meals[0] if meals else None

def get_random_meal():
    response = requests.get(f"{API_BASE}/random.php")
    meals = response.json().get("meals",[])
    return meals[0] if meals else None